from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegisterForm, ProfileForm
from app.models.user import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Pagina di login"""
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Benvenuto {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('shop.index'))
        else:
            flash('Email o password non validi', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Pagina di registrazione"""
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registrazione completata! Ora puoi effettuare il login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout dell'utente"""
    logout_user()
    flash('Logout effettuato con successo', 'info')
    return redirect(url_for('shop.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Pagina profilo utente"""
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.postal_code = form.postal_code.data
        current_user.country = form.country.data
        db.session.commit()
        flash('Profilo aggiornato con successo!', 'success')
        return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        # Popola il form con i dati attuali
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone.data = current_user.phone
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.postal_code.data = current_user.postal_code
        form.country.data = current_user.country

    return render_template('auth/profile.html', form=form)


@auth_bp.route('/orders')
@login_required
def orders():
    """Lista ordini dell'utente"""
    orders = current_user.orders.order_by(db.desc('created_at')).all()
    return render_template('auth/orders.html', orders=orders)
