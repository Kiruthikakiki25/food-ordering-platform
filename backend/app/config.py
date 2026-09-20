import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # Comma-separated list of frontend origins allowed by CORS
    CORS_ORIGINS = [
        o.strip() for o in os.getenv(
            'CORS_ORIGINS',
            'https://food-ordering-platform-kohl.vercel.app,http://localhost:5173'
        ).split(',') if o.strip()
    ]


class TestConfig:
    """Used by automated tests only: temporary in-memory database, no email."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False},
        'poolclass': __import__('sqlalchemy.pool', fromlist=['StaticPool']).StaticPool,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key-for-automated-tests-only'
    JWT_SECRET_KEY = 'test-jwt-secret-key-for-automated-tests-only-123'
    MAIL_USERNAME = None
    CORS_ORIGINS = ['http://localhost:5173']