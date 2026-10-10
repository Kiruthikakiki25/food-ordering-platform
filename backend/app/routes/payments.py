from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
import os
from app.models import Order, Payment, db

payments_bp = Blueprint('payments', __name__)

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


@payments_bp.route('/payments/create-payment-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    user_id = get_jwt_identity()
    order_id = request.json.get('order_id')

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.total * 100),  # convert to paise
            currency='inr',
            metadata={'order_id': order_id}
        )
        return jsonify({
            'client_secret': intent.client_secret,
            'amount': order.total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/payments/confirm', methods=['POST'])
@jwt_required()
def confirm_payment():
    user_id = get_jwt_identity()
    order_id = request.json.get('order_id')

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.status = 'preparing'
    payment = Payment(
        order_id=order_id,
        stripe_payment_intent_id=request.json.get('payment_intent_id', ''),
        status='paid'
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({'message': 'Payment confirmed'})


@payments_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify({'error': 'invalid signature'}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        if order_id:
            order = Order.query.get(order_id)
            if order:
                order.status = 'paid'
                db.session.commit()

    return jsonify({'received': True}), 200