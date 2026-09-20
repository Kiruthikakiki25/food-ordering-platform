from flask import Blueprint, jsonify, request
from app.models import MenuItem

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/menu', methods=['GET'])
def list_menu():
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify([_serialize(item) for item in items])


@menu_bp.route('/menu/search', methods=['GET'])
def search_menu():
    q = request.args.get('q', '')
    category = request.args.get('category')

    query = MenuItem.query.filter_by(is_available=True)
    if q:
        query = query.filter(MenuItem.name.ilike(f"%{q}%"))
    if category:
        query = query.filter_by(category=category)

    items = query.all()
    return jsonify([_serialize(item) for item in items])


@menu_bp.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    return jsonify(_serialize(item))


def _serialize(item):
    return {
        "id": item.id,
        "name": item.name,
        "category": item.category,
        "price": item.price,
        "veg_flag": item.veg_flag,
        "cuisine_tags": item.cuisine_tags,
        "description": item.description,
    }