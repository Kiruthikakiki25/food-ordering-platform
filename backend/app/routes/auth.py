import re
import os
import threading
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from app import db, mail
from app.models import User
from app.utils.tokens import generate_token, verify_token
from flask_mail import Message

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')

HASH_METHOD = 'pbkdf2:sha256'  # light on memory, safe for the free Render plan


def _send_async(app, subject, recipient, body):
    with app.app_context():
        try:
            msg = Message(subject, recipients=[recipient], body=body)
            mail.send(msg)
        except Exception as e:
            app.logger.error(f"Mail send failed: {e}")


def send_email(subject, recipient, body):
    """Sends via Flask-Mail in a background thread; never blocks or breaks the request."""
    app = current_app._get_current_object()
    if app.config.get('MAIL_USERNAME'):
        threading.Thread(
            target=_send_async, args=(app, subject, recipient, body), daemon=True
        ).start()
    else:
        app.logger.info(f"[DEV EMAIL] To: {recipient}\nSubject: {subject}\n{body}")


def _base_url():
    """Public backend URL. Set BACKEND_URL on Render; falls back to the request host."""
    url = os.environ.get('BACKEND_URL')
    if url:
        return url.rstrip('/') + '/'
    return request.host_url


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'name, email, and password are required'}), 400

    try:
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    if not PASSWORD_REGEX.match(password):
        return jsonify({
            'error': 'Password must be 8+ characters with at least one uppercase letter, one lowercase letter, and one number'
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password, method=HASH_METHOD),
        is_verified=False
    )
    db.session.add(user)
    db.session.commit()

    token = generate_token(email, salt='email-verify')
    verify_link = f"{_base_url()}auth/verify-email/{token}"
    send_email(
        subject="Verify your email",
        recipient=email,
        body=f"Click to verify your account: {verify_link}"
    )

    return jsonify({
        'message': 'Registered. Check your email to verify your account.',
        'user_id': user.id
    }), 201


@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    email = verify_token(token, salt='email-verify', max_age=3600)
    if not email:
        return jsonify({'error': 'Invalid or expired verification link'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_verified = True
    db.session.commit()
    return jsonify({'message': 'Email verified. You can now log in.'}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_verified:
        return jsonify({'error': 'Please verify your email before logging in'}), 403

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {'id': user.id, 'name': user.name, 'email': user.email}
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({'access_token': new_access_token}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    # Always return 200 even if user doesn't exist, to avoid leaking which emails are registered
    if user:
        token = generate_token(email, salt='password-reset')
        reset_link = f"{_base_url()}auth/reset-password/{token}"
        send_email(
            subject="Reset your password",
            recipient=email,
            body=f"Click to reset your password: {reset_link}"
        )

    return jsonify({'message': 'If that email is registered, a reset link has been sent.'}), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    email = verify_token(token, salt='password-reset', max_age=1800)
    if not email:
        return jsonify({'error': 'Invalid or expired reset link'}), 400

    data = request.get_json()
    new_password = data.get('password')

    if not PASSWORD_REGEX.match(new_password):
        return jsonify({
            'error': 'Password must be 8+ characters with at least one uppercase letter, one lowercase letter, and one number'
        }), 400

    user = User.query.filter_by(email=email).first()
    user.password_hash = generate_password_hash(new_password, method=HASH_METHOD)
    db.session.commit()

    return jsonify({'message': 'Password reset successful. You can now log in.'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200