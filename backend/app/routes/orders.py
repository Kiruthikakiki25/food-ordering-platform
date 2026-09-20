from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, OrderItem, MenuItem, Branch

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.json

    branch_id = data.get('branch_id')
    cart_items = data.get('items', [])  # [{ "menu_item_id": 1, "quantity": 2 }, ...]

    if not branch_id:
        return jsonify({"error": "branch_id is required"}), 400
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    branch = Branch.query.get(branch_id)
    if not branch or not branch.is_active:
        return jsonify({"error": "Invalid or inactive branch"}), 400

    order = Order(user_id=user_id, branch_id=branch_id, status='placed', total=0)
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    total = 0
    for ci in cart_items:
        menu_item = MenuItem.query.get(ci['menu_item_id'])
        if not menu_item or not menu_item.is_available:
            db.session.rollback()
            return jsonify({"error": f"Menu item {ci['menu_item_id']} unavailable"}), 400

        quantity = ci.get('quantity', 1)
        line_total = menu_item.price * quantity
        total += line_total

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=quantity,
            price_at_order=menu_item.price
        )
        db.session.add(order_item)

    order.total = total
    db.session.commit()

    return jsonify({"order_id": order.id, "total": order.total, "status": order.status}), 201


@orders_bp.route('/orders/my-orders', methods=['GET'])
@jwt_required()
def my_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([_serialize_order(o) for o in orders])


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    if str(order.user_id) != str(user_id):
        return jsonify({"error": "Not authorized"}), 403
    return jsonify(_serialize_order(order))


@orders_bp.route('/orders/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.json.get('status')

    valid_statuses = ['placed', 'preparing', 'out_for_delivery', 'delivered']
    if new_status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    order.status = new_status
    db.session.commit()
    return jsonify({"order_id": order.id, "status": order.status})


def _serialize_order(order):
    return {
        "id": order.id,
        "branch": {
            "id": order.branch.id,
            "name": order.branch.name,
            "city": order.branch.city,
        },
        "status": order.status,
        "total": order.total,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "menu_item_id": oi.menu_item_id,
                "name": oi.menu_item.name,
                "quantity": oi.quantity,
                "price_at_order": oi.price_at_order,
            }
            for oi in order.items
        ],
    }