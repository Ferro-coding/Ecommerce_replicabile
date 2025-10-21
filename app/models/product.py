from datetime import datetime
from app import db


class Category(db.Model):
    """Modello per categorie prodotti"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))

    # Relazioni
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    """Modello per prodotti"""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500))

    # Prezzi
    price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float)
    cost = db.Column(db.Float)  # Costo di acquisto

    # Inventario
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True)

    # Immagini (separare con virgola per multiple immagini)
    image = db.Column(db.String(200))
    images = db.Column(db.Text)  # JSON o CSV di immagini

    # Categoria
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # Attributi
    weight = db.Column(db.Float)  # in kg
    dimensions = db.Column(db.String(100))  # es: "30x20x10"

    # Stato
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relazioni
    cart_items = db.relationship('Cart', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

    @property
    def current_price(self):
        """Ritorna il prezzo attuale (sale_price se disponibile, altrimenti price)"""
        return self.sale_price if self.sale_price else self.price

    @property
    def discount_percentage(self):
        """Calcola la percentuale di sconto"""
        if self.sale_price and self.price > self.sale_price:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0

    @property
    def in_stock(self):
        """Verifica se il prodotto è disponibile"""
        return self.stock > 0

    def __repr__(self):
        return f'<Product {self.name}>'
