import os
from datetime import timedelta

class Config:
    """Configurazione base - MODIFICA QUESTI VALORI PER OGNI PROGETTO"""

    # Nome del progetto - PERSONALIZZA
    PROJECT_NAME = "Ecommerce Template"

    # Secret Key - CAMBIA QUESTA IN PRODUZIONE
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Pagination
    PRODUCTS_PER_PAGE = 12
    ORDERS_PER_PAGE = 20

    # Upload
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Email (configurare per invio email)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Pagamenti - CONFIGURA CON LE TUE CHIAVI
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

    # IVA e tasse - PERSONALIZZA
    TAX_RATE = 0.22  # 22% IVA italiana
    SHIPPING_COST = 5.00
    FREE_SHIPPING_THRESHOLD = 50.00

    # Valuta
    CURRENCY = 'EUR'
    CURRENCY_SYMBOL = '€'


class DevelopmentConfig(Config):
    """Configurazione per sviluppo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configurazione per produzione"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Configurazione per testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
