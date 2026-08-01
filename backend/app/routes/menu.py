from flask import Blueprint, request, jsonify
from app.models import Restaurant, MenuItem

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/restaurants', methods=['GET'])
def list_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'cuisine': r.cuisine,
        'rating': r.rating
    } for r in restaurants]), 200


@menu_bp.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    if not items:
        return jsonify({'message': 'No menu items found for this restaurant'}), 404

    return jsonify([{
        'id': i.id,
        'name': i.name,
        'category': i.category,
        'price': i.price,
        'veg_flag': i.veg_flag
    } for i in items]), 200


@menu_bp.route('/menu/search', methods=['GET'])
def search_menu():
    query = request.args.get('q', '')
    cuisine = request.args.get('cuisine', '')

    q = MenuItem.query
    if query:
        q = q.filter(MenuItem.name.ilike(f'%{query}%'))
    if cuisine:
        q = q.join(Restaurant).filter(Restaurant.cuisine.ilike(f'%{cuisine}%'))

    results = q.all()
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'category': i.category,
        'price': i.price
    } for i in results]), 200