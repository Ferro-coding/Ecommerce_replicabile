from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.cart import cart_bp
from app.models.cart import Cart
from app.models.product import Product
from app.models.order import Order, OrderItem
from datetime import datetime
import uuid


@cart_bp.route('/')
@login_required
def view():
    """Visualizza carrello"""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    # Calcola totali
    subtotal = sum(item.subtotal for item in cart_items)
    tax = subtotal * current_app.config['TAX_RATE']
    shipping = current_app.config['SHIPPING_COST']

    # Spedizione gratuita oltre soglia
    if subtotal >= current_app.config['FREE_SHIPPING_THRESHOLD']:
        shipping = 0

    total = subtotal + tax + shipping

    return render_template('cart/view.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add(product_id):
    """Aggiungi prodotto al carrello"""
    product = Product.query.get_or_404(product_id)

    if not product.is_active:
        flash('Prodotto non disponibile', 'danger')
        return redirect(url_for('shop.products'))

    quantity = request.form.get('quantity', 1, type=int)

    if quantity < 1:
        flash('Quantità non valida', 'danger')
        return redirect(url_for('shop.product_detail', slug=product.slug))

    if product.stock < quantity:
        flash('Quantità non disponibile in magazzino', 'danger')
        return redirect(url_for('shop.product_detail', slug=product.slug))

    # Verifica se il prodotto è già nel carrello
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        # Aggiorna quantità
        new_quantity = cart_item.quantity + quantity
        if product.stock < new_quantity:
            flash('Quantità non disponibile in magazzino', 'danger')
            return redirect(url_for('shop.product_detail', slug=product.slug))
        cart_item.quantity = new_quantity
    else:
        # Crea nuovo item
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} aggiunto al carrello!', 'success')

    return redirect(url_for('cart.view'))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update(item_id):
    """Aggiorna quantità nel carrello"""
    cart_item = Cart.query.get_or_404(item_id)

    if cart_item.user_id != current_user.id:
        abort(403)

    quantity = request.form.get('quantity', 1, type=int)

    if quantity < 1:
        # Rimuovi se quantità < 1
        db.session.delete(cart_item)
        flash('Prodotto rimosso dal carrello', 'info')
    else:
        if cart_item.product.stock < quantity:
            flash('Quantità non disponibile in magazzino', 'danger')
            return redirect(url_for('cart.view'))
        cart_item.quantity = quantity
        flash('Carrello aggiornato', 'success')

    db.session.commit()
    return redirect(url_for('cart.view'))


@cart_bp.route('/remove/<int:item_id>')
@login_required
def remove(item_id):
    """Rimuovi prodotto dal carrello"""
    cart_item = Cart.query.get_or_404(item_id)

    if cart_item.user_id != current_user.id:
        abort(403)

    db.session.delete(cart_item)
    db.session.commit()
    flash('Prodotto rimosso dal carrello', 'info')

    return redirect(url_for('cart.view'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Pagina checkout"""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Il carrello è vuoto', 'warning')
        return redirect(url_for('shop.products'))

    # Calcola totali
    subtotal = sum(item.subtotal for item in cart_items)
    tax = subtotal * current_app.config['TAX_RATE']
    shipping = current_app.config['SHIPPING_COST']

    if subtotal >= current_app.config['FREE_SHIPPING_THRESHOLD']:
        shipping = 0

    total = subtotal + tax + shipping

    if request.method == 'POST':
        # Crea ordine
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

        order = Order(
            order_number=order_number,
            user_id=current_user.id,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping,
            total=total,
            shipping_first_name=request.form.get('first_name'),
            shipping_last_name=request.form.get('last_name'),
            shipping_email=request.form.get('email'),
            shipping_phone=request.form.get('phone'),
            shipping_address=request.form.get('address'),
            shipping_city=request.form.get('city'),
            shipping_postal_code=request.form.get('postal_code'),
            shipping_country=request.form.get('country', 'Italia'),
            notes=request.form.get('notes'),
            payment_method=request.form.get('payment_method', 'bank_transfer')
        )

        db.session.add(order)
        db.session.flush()  # Per ottenere l'ID dell'ordine

        # Crea order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                price=cart_item.product.current_price,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)

            # Aggiorna stock prodotto
            cart_item.product.stock -= cart_item.quantity

        # Svuota carrello
        Cart.query.filter_by(user_id=current_user.id).delete()

        db.session.commit()

        flash(f'Ordine {order_number} creato con successo!', 'success')
        return redirect(url_for('cart.order_confirmation', order_id=order.id))

    return render_template('cart/checkout.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)


@cart_bp.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Conferma ordine"""
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        abort(403)

    return render_template('cart/order_confirmation.html', order=order)
