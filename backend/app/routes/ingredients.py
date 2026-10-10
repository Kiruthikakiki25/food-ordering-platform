from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from groq import Groq
from app.models import MenuItem, Ingredient, AllergenProfile, Order, OrderItem, db
import os, json

ingredients_bp = Blueprint('ingredients', __name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


@ingredients_bp.route('/menu/<int:item_id>/ingredients', methods=['GET'])
def get_ingredients(item_id):
    item = MenuItem.query.get_or_404(item_id)
    ingredients = Ingredient.query.filter_by(menu_item_id=item_id).all()

    user_allergens = []
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            profile = AllergenProfile.query.filter_by(user_id=user_id).first()
            if profile:
                user_allergens = profile.allergens or []
    except Exception:
        pass

    ingredient_list = []
    for ing in ingredients:
        flagged = any(a in user_allergens for a in (ing.allergen_flags or []))
        ingredient_list.append({
            "name": ing.name,
            "allergen_flags": ing.allergen_flags or [],
            "flagged_for_user": flagged
        })

    return jsonify({
        "item_name": item.name,
        "ingredients": ingredient_list,
        "nutrition": item.nutrition_info,
        "calories": item.calorie_count,
        "user_allergens": user_allergens
    })


@ingredients_bp.route('/menu/<int:item_id>/ask', methods=['POST'])
def ask_about_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    ingredients = Ingredient.query.filter_by(menu_item_id=item_id).all()
    ingredient_text = ", ".join([i.name for i in ingredients])
    allergens_present = list(set(
        flag for ing in ingredients for flag in (ing.allergen_flags or [])
    ))

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful food assistant. Answer questions about this dish based only on the ingredient information provided.

Dish: {item.name}
Ingredients: {ingredient_text}
Allergens present: {allergens_present}
Nutrition: {item.nutrition_info}

Be specific, honest, and concise. If you cannot determine something from the ingredient list, say so clearly.
Never give medical advice — only ingredient-based factual answers. Keep reply under 3 sentences."""
            },
            {"role": "user", "content": question}
        ],
        temperature=0.4,
        max_tokens=1000
    )

    return jsonify({"answer": response.choices[0].message.content.strip()})


@ingredients_bp.route('/restaurants/<int:restaurant_id>/smart-search', methods=['POST'])
def smart_menu_search(restaurant_id):
    query = request.json.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    items = MenuItem.query.filter_by(is_available=True).all()
    menu_data = []
    for item in items:
        ingredients = Ingredient.query.filter_by(menu_item_id=item.id).all()
        menu_data.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "category": item.category,
            "veg": item.veg_flag,
            "calories": item.calorie_count,
            "nutrition": item.nutrition_info,
            "allergens": list(set(
                flag for ing in ingredients for flag in (ing.allergen_flags or [])
            ))
        })

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": f"""You are a food intelligence assistant. Given this restaurant menu, answer the user's query.

Menu: {json.dumps(menu_data, indent=2)}

Return ONLY valid JSON — no markdown, no explanation:
{{
  "recommendations": [
    {{"id": 1, "name": "...", "price": 0.0, "reason": "one short sentence"}}
  ],
  "explanation": "brief overall explanation"
}}"""
            },
            {"role": "user", "content": query}
        ],
        temperature=0.3,
        max_tokens=2000
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return jsonify(json.loads(raw.strip()))


@ingredients_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()

    past_items = (
        db.session.query(MenuItem)
        .join(OrderItem, OrderItem.menu_item_id == MenuItem.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.user_id == user_id)
        .all()
    )

    all_items = MenuItem.query.filter_by(is_available=True).all()
    catalog = [
        {"id": i.id, "name": i.name, "category": i.category,
         "price": i.price, "veg": i.veg_flag}
        for i in all_items
    ]

    if not past_items:
        defaults = MenuItem.query.filter_by(is_available=True).limit(5).all()
        return jsonify([
            {"id": i.id, "name": i.name, "category": i.category,
             "price": i.price, "reason": "Popular choice"}
            for i in defaults
        ])

    ordered_names = [i.name for i in past_items]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{
            "role": "user",
            "content": f"""A user previously ordered: {ordered_names}.
From this menu catalog, recommend 4 different items they haven't ordered yet.
Catalog: {json.dumps(catalog)}
Return ONLY valid JSON — a list, no markdown:
[{{"id": 1, "name": "...", "category": "...", "price": 0.0, "reason": "one short sentence"}}]"""
        }],
        temperature=0.4,
        max_tokens=2000
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return jsonify(json.loads(raw.strip()))
