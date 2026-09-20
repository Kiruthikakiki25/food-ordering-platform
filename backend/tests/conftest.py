import pytest
from email_validator import EmailNotValidError
from app import create_app, db
from app.config import TestConfig
from app.models import Branch, MenuItem, User


@pytest.fixture()
def app(monkeypatch):
    # Skip the DNS lookup inside validate_email so tests work offline
    def fake_validate(email, **kwargs):
        if '@' not in email:
            raise EmailNotValidError('invalid email')
    monkeypatch.setattr('app.routes.auth.validate_email', fake_validate)

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        db.session.add_all([
            Branch(name='Cantonment', address='12 Cantonment Rd', city='Trichy', pincode='620001'),
            Branch(name='Thillai Nagar', address='45 Thillai Nagar Main Rd', city='Trichy', pincode='620018'),
            MenuItem(name='Paneer Butter Masala', category='Main Course', price=220.0, veg_flag=True),
            MenuItem(name='Chicken Biryani', category='Main Course', price=260.0, veg_flag=False),
            MenuItem(name='Filter Coffee', category='Beverages', price=30.0, veg_flag=True),
        ])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def verified_user(app):
    """Registers a user through the API, then marks them verified."""
    c = app.test_client()
    c.post('/auth/register', json={
        'name': 'Test User', 'email': 'test@example.com', 'password': 'Passw0rdX'
    })
    with app.app_context():
        u = User.query.filter_by(email='test@example.com').first()
        u.is_verified = True
        db.session.commit()
    return {'email': 'test@example.com', 'password': 'Passw0rdX'}