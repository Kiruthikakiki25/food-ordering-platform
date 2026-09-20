import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import text
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(level=logging.INFO)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config.get('CORS_ORIGINS', []))

    from app import models  # registers models before create_all

    from app.routes.auth import auth_bp
    from app.routes.menu import menu_bp
    from app.routes.orders import orders_bp
    from app.routes.payments import payments_bp
    from app.routes.branches import branches_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(branches_bp)

    @app.route('/health', methods=['GET'])
    def health():
        """Service status for monitoring; also checks the database connection."""
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({'status': 'OK', 'database': 'connected'}), 200
        except Exception as e:
            app.logger.error(f'Health check failed: {e}')
            return jsonify({'status': 'ERROR', 'database': 'unreachable'}), 503

    return app