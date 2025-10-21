from flask import Blueprint

shop_bp = Blueprint('shop', __name__, template_folder='../templates/shop')

from app.shop import routes
