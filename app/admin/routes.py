from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.admin import admin_bp
from app.utils.decorators import admin_required
from app.models.product import Product, Category
from app.models.order import Order
from app.models.user import User
from sqlalchemy import func


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Dashboard amministrativo"""
    # Statistiche
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total)).filter_by(payment_status='paid').scalar() or 0
    total_products = Product.query.count()
    total_users = User.query.count()

    # Ordini recenti
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    # Prodotti con stock basso
    low_stock_products = Product.query.filter(Product.stock < 10, Product.is_active == True).all()

    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_products=total_products,
                         total_users=total_users,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products)


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """Lista ordini"""
    page = request.args.get('page', 1, type=int)
    per_page = request.current_app.config['ORDERS_PER_PAGE']

    status = request.args.get('status')
    query = Order.query

    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    orders = pagination.items

    return render_template('admin/orders.html', orders=orders, pagination=pagination)


@admin_bp.route('/order/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    """Dettaglio ordine"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@admin_bp.route('/order/<int:order_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """Aggiorna stato ordine"""
    order = Order.query.get_or_404(order_id)

    status = request.form.get('status')
    payment_status = request.form.get('payment_status')
    tracking_number = request.form.get('tracking_number')
    admin_notes = request.form.get('admin_notes')

    if status:
        order.status = status
    if payment_status:
        order.payment_status = payment_status
    if tracking_number:
        order.tracking_number = tracking_number
    if admin_notes:
        order.admin_notes = admin_notes

    db.session.commit()
    flash('Ordine aggiornato con successo', 'success')

    return redirect(url_for('admin.order_detail', order_id=order_id))


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """Lista prodotti"""
    page = request.args.get('page', 1, type=int)
    per_page = request.current_app.config['PRODUCTS_PER_PAGE']

    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    products = pagination.items
    categories = Category.query.all()

    return render_template('admin/products.html', products=products, pagination=pagination, categories=categories)


@admin_bp.route('/product/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    """Aggiungi prodotto"""
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            slug=request.form.get('slug'),
            description=request.form.get('description'),
            short_description=request.form.get('short_description'),
            price=float(request.form.get('price')),
            sale_price=float(request.form.get('sale_price')) if request.form.get('sale_price') else None,
            stock=int(request.form.get('stock', 0)),
            sku=request.form.get('sku'),
            category_id=int(request.form.get('category_id')) if request.form.get('category_id') else None,
            is_active=request.form.get('is_active') == 'on',
            is_featured=request.form.get('is_featured') == 'on'
        )

        db.session.add(product)
        db.session.commit()
        flash('Prodotto aggiunto con successo', 'success')

        return redirect(url_for('admin.products'))

    categories = Category.query.all()
    return render_template('admin/product_form.html', categories=categories)


@admin_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """Modifica prodotto"""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.slug = request.form.get('slug')
        product.description = request.form.get('description')
        product.short_description = request.form.get('short_description')
        product.price = float(request.form.get('price'))
        product.sale_price = float(request.form.get('sale_price')) if request.form.get('sale_price') else None
        product.stock = int(request.form.get('stock', 0))
        product.sku = request.form.get('sku')
        product.category_id = int(request.form.get('category_id')) if request.form.get('category_id') else None
        product.is_active = request.form.get('is_active') == 'on'
        product.is_featured = request.form.get('is_featured') == 'on'

        db.session.commit()
        flash('Prodotto aggiornato con successo', 'success')

        return redirect(url_for('admin.products'))

    categories = Category.query.all()
    return render_template('admin/product_form.html', product=product, categories=categories)


@admin_bp.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    """Elimina prodotto"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Prodotto eliminato con successo', 'success')

    return redirect(url_for('admin.products'))


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """Lista categorie"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Lista utenti"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    users = pagination.items

    return render_template('admin/users.html', users=users, pagination=pagination)
