from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    from app import models  # registers models before create_all

    from app.routes.auth import auth_bp
    from app.routes.menu import menu_bp
    from app.routes.orders import orders_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orders_bp)

    return app