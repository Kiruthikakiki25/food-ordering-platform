import stripe
import os
import threading
import time
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, Payment

payments_bp = Blueprint('payments', __name__)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@payments_bp.route('/payments/create-payment-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    data = request.get_json()
    order_id = data.get('order_id')

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    user_id = get_jwt_identity()
    if str(order.user_id) != str(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    amount_in_cents = int(order.total * 100)

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency='inr',
            metadata={'order_id': order.id}
        )
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400

    payment = Payment(
        order_id=order.id,
        stripe_payment_intent_id=intent.id,
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'client_secret': intent.client_secret,
        'payment_id': payment.id,
        'amount': order.total
    }), 201


def auto_advance_order(app, order_id):
    stages = ['preparing', 'out_for_delivery', 'delivered']
    with app.app_context():
        for stage in stages:
            time.sleep(15)  # 15 seconds between each stage
            order = Order.query.get(order_id)
            if order:
                order.status = stage
                db.session.commit()


@payments_bp.route('/payments/confirm', methods=['POST'])
@jwt_required()
def confirm_payment():
    data = request.get_json()
    order_id = data.get('order_id')

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    payment = Payment.query.filter_by(order_id=order_id).first()
    if payment:
        payment.status = 'succeeded'
    order.status = 'placed'
    db.session.commit()

    app = current_app._get_current_object()
    threading.Thread(target=auto_advance_order, args=(app, order.id)).start()

    return jsonify({'message': 'Payment confirmed, order progressing'}), 200