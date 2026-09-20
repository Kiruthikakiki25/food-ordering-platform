from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='customer')  # customer | staff (optional, per branch)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True)


class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)        # e.g. "Anna Nagar", "T Nagar"
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)

    orders = db.relationship('Order', backref='branch', lazy=True)


class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))          # e.g. Starters, Main Course, Desserts
    price = db.Column(db.Float, nullable=False)
    veg_flag = db.Column(db.Boolean, default=True)
    cuisine_tags = db.Column(db.String(100))
    description = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)   # brand-wide availability toggle
    # No branch_id / restaurant_id — menu is shared across every branch

    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    status = db.Column(db.String(20), default='placed')  # placed -> preparing -> out_for_delivery -> delivered
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_order = db.Column(db.Float, nullable=False)  # snapshot price, in case menu price changes later


class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    stripe_payment_intent_id = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending | succeeded | failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    