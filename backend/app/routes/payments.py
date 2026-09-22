from flask import Blueprint, request, jsonify
import stripe
import os

payments_bp = Blueprint('payments', __name__)
@payments_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify({"error": "invalid signature"}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')

        if not order_id:
            return jsonify({"received": True}), 200

        order = Order.query.get(order_id)
        if order:
            order.status = 'paid'
            db.session.commit()

    return jsonify({"received": True}), 200