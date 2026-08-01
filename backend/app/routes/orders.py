from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, OrderItem, MenuItem

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

VALID_STATUSES = ['placed', 'preparing', 'out_for_delivery', 'delivered']


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    items = data.get('items')  # [{menu_item_id, quantity}, ...]

    if not items or not isinstance(items, list):
        return jsonify({'error': 'items must be a non-empty list of {menu_item_id, quantity}'}), 400

    total = 0
    order_items_to_create = []

    for entry in items:
        menu_item_id = entry.get('menu_item_id')
        quantity = entry.get('quantity', 1)

        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            return jsonify({'error': f'Menu item {menu_item_id} not found'}), 404
        if quantity < 1:
            return jsonify({'error': f'Invalid quantity for menu item {menu_item_id}'}), 400

        total += menu_item.price * quantity
        order_items_to_create.append((menu_item_id, quantity))

    order = Order(user_id=int(user_id), status='placed', total=total)
    db.session.add(order)
    db.session.flush()  # gets order.id before commit

    for menu_item_id, quantity in order_items_to_create:
        db.session.add(OrderItem(order_id=order.id, menu_item_id=menu_item_id, quantity=quantity))

    db.session.commit()

    return jsonify({
        'message': 'Order placed',
        'order_id': order.id,
        'total': total,
        'status': order.status
    }), 201


@orders_bp.route('/my-orders', methods=['GET'])
@jwt_required()
def my_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=int(user_id)).order_by(Order.created_at.desc()).all()

    return jsonify([{
        'id': o.id,
        'status': o.status,
        'total': o.total,
        'created_at': o.created_at.isoformat()
    } for o in orders]), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order or order.user_id != int(user_id):
        return jsonify({'error': 'Order not found'}), 404

    items = OrderItem.query.filter_by(order_id=order.id).all()
    return jsonify({
        'id': order.id,
        'status': order.status,
        'total': order.total,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'menu_item_id': i.menu_item_id,
            'quantity': i.quantity
        } for i in items]
    }), 200


@orders_bp.route('/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_status(order_id):
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in VALID_STATUSES:
        return jsonify({'error': f'Status must be one of {VALID_STATUSES}'}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.status = new_status
    db.session.commit()

    return jsonify({'message': 'Status updated', 'order_id': order.id, 'status': order.status}), 200