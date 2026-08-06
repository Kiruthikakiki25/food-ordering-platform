import stripe
import os
from flask import Blueprint, request, jsonify
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
            currency='usd',
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
        'payment_id': payment.id
    }), 201