from flask import render_template, request, abort, current_app
from app.shop import shop_bp
from app.models.product import Product, Category
from sqlalchemy import or_


@shop_bp.route('/')
def index():
    """Homepage con prodotti in evidenza"""
    featured_products = Product.query.filter_by(is_active=True, is_featured=True).limit(8).all()
    categories = Category.query.all()
    return render_template('shop/index.html', featured_products=featured_products, categories=categories)


@shop_bp.route('/products')
def products():
    """Catalogo prodotti con filtri e paginazione"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PRODUCTS_PER_PAGE']

    # Filtri
    category_slug = request.args.get('category')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')

    # Query base
    query = Product.query.filter_by(is_active=True)

    # Filtro categoria
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=category.id)

    # Filtro ricerca
    if search:
        query = query.filter(or_(
            Product.name.ilike(f'%{search}%'),
            Product.description.ilike(f'%{search}%')
        ))

    # Ordinamento
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name':
        query = query.order_by(Product.name.asc())
    else:  # newest
        query = query.order_by(Product.created_at.desc())

    # Paginazione
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items

    categories = Category.query.all()

    return render_template('shop/products.html',
                         products=products,
                         pagination=pagination,
                         categories=categories,
                         current_category=category_slug,
                         search=search,
                         sort=sort)


@shop_bp.route('/product/<slug>')
def product_detail(slug):
    """Dettaglio prodotto"""
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()

    # Prodotti correlati (stessa categoria)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()

    return render_template('shop/product_detail.html', product=product, related_products=related_products)


@shop_bp.route('/category/<slug>')
def category(slug):
    """Prodotti per categoria"""
    category = Category.query.filter_by(slug=slug).first_or_404()

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PRODUCTS_PER_PAGE']

    pagination = Product.query.filter_by(
        category_id=category.id,
        is_active=True
    ).order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    products = pagination.items
    categories = Category.query.all()

    return render_template('shop/category.html',
                         category=category,
                         products=products,
                         pagination=pagination,
                         categories=categories)
