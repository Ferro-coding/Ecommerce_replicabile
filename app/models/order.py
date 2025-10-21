from datetime import datetime
from app import db


class Order(db.Model):
    """Modello per ordini"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Utente
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Totali
    subtotal = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)

    # Stato ordine
    status = db.Column(db.String(20), default='pending')  # pending, processing, shipped, delivered, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    payment_method = db.Column(db.String(50))

    # Informazioni spedizione
    shipping_first_name = db.Column(db.String(50), nullable=False)
    shipping_last_name = db.Column(db.String(50), nullable=False)
    shipping_email = db.Column(db.String(120), nullable=False)
    shipping_phone = db.Column(db.String(20))
    shipping_address = db.Column(db.String(200), nullable=False)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_postal_code = db.Column(db.String(20), nullable=False)
    shipping_country = db.Column(db.String(50), nullable=False)

    # Note
    notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)

    # Tracking
    tracking_number = db.Column(db.String(100))

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)

    # Relazioni
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """Modello per item di un ordine"""

    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Salviamo i dettagli del prodotto al momento dell'ordine
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    @property
    def subtotal(self):
        """Calcola il subtotale per questo item"""
        return self.price * self.quantity

    def __repr__(self):
        return f'<OrderItem order={self.order_id} product={self.product_name}>'
