from datetime import datetime
from app import db


class Cart(db.Model):
    """Modello per carrello della spesa"""

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def subtotal(self):
        """Calcola il subtotale per questo item"""
        return self.product.current_price * self.quantity

    def __repr__(self):
        return f'<Cart user={self.user_id} product={self.product_id} qty={self.quantity}>'
