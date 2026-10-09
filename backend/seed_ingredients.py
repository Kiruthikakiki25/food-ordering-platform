"""
seed_ingredients.py — Auto-generates ingredients + nutrition for every
MenuItem using Groq/Llama. Run once after flask db upgrade.

Run: python seed_ingredients.py
"""

import os, json
from groq import Groq
from app import create_app, db
from app.models import MenuItem, Ingredient

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

ALLERGEN_LIST = ["peanuts", "gluten", "dairy", "eggs", "shellfish", "soy", "MSG"]


def generate(item_name, cuisine, category):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{
            "role": "user",
            "content": f"""List realistic ingredients for: {item_name} ({cuisine}, {category}).
Flag allergens from this list only: {ALLERGEN_LIST}.
Return ONLY valid JSON — no explanation, no markdown:
{{
  "ingredients": [
    {{"name": "refined flour", "allergen_flags": ["gluten"]}},
    {{"name": "butter", "allergen_flags": ["dairy"]}},
    {{"name": "salt", "allergen_flags": []}}
  ],
  "nutrition": {{"calories": 320, "protein": 8, "carbs": 45, "fat": 12, "fiber": 2}}
}}"""
        }],
        temperature=0.3,
        max_tokens=2000
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


app = create_app()
with app.app_context():
    items = MenuItem.query.all()
    for item in items:
        # Skip if already seeded
        if Ingredient.query.filter_by(menu_item_id=item.id).first():
            print(f"  Skipping {item.name} (already seeded)")
            continue

        print(f"  Seeding: {item.name}...")
        try:
            data = generate(item.name, item.cuisine_tags or "", item.category or "")
            for ing in data["ingredients"]:
                db.session.add(Ingredient(
                    menu_item_id=item.id,
                    name=ing["name"],
                    allergen_flags=ing.get("allergen_flags", [])
                ))
            item.calorie_count = data["nutrition"]["calories"]
            item.nutrition_info = data["nutrition"]
            db.session.commit()
            print(f"    ✓ {len(data['ingredients'])} ingredients, {data['nutrition']['calories']} kcal")
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            db.session.rollback()

print("\nDone.")
