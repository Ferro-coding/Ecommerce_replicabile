from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Inizializza estensioni
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='default'):
    """
    Factory pattern per creare l'applicazione Flask

    Args:
        config_name: Nome della configurazione da usare (development, production, testing)

    Returns:
        app: Istanza Flask configurata
    """
    app = Flask(__name__)

    # Carica configurazione
    app.config.from_object(config[config_name])

    # Inizializza estensioni con app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configurazione login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Effettua il login per accedere a questa pagina.'
    login_manager.login_message_category = 'info'

    # Registra blueprint
    from app.auth import auth_bp
    from app.shop import shop_bp
    from app.cart import cart_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(shop_bp, url_prefix='/')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Context processor per variabili globali nei template
    @app.context_processor
    def inject_globals():
        from flask_login import current_user
        cart_count = 0
        if current_user.is_authenticated:
            from app.models.cart import Cart
            cart_items = Cart.query.filter_by(user_id=current_user.id).all()
            cart_count = sum(item.quantity for item in cart_items)

        return {
            'PROJECT_NAME': app.config['PROJECT_NAME'],
            'CURRENCY_SYMBOL': app.config['CURRENCY_SYMBOL'],
            'cart_count': cart_count
        }

    # Crea tabelle database al primo avvio
    with app.app_context():
        db.create_all()

    return app
