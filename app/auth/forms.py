from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models.user import User


class LoginForm(FlaskForm):
    """Form di login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Accedi')


class RegisterForm(FlaskForm):
    """Form di registrazione"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username deve essere tra 3 e 80 caratteri')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='La password deve essere di almeno 6 caratteri')
    ])
    password2 = PasswordField('Conferma Password', validators=[
        DataRequired(),
        EqualTo('password', message='Le password devono coincidere')
    ])
    submit = SubmitField('Registrati')

    def validate_username(self, username):
        """Verifica che l'username non sia già in uso"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username già in uso. Scegli un altro username.')

    def validate_email(self, email):
        """Verifica che l'email non sia già in uso"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email già registrata. Usa un\'altra email o effettua il login.')


class ProfileForm(FlaskForm):
    """Form per modificare il profilo utente"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nome', validators=[Length(max=50)])
    last_name = StringField('Cognome', validators=[Length(max=50)])
    phone = StringField('Telefono', validators=[Length(max=20)])
    address = StringField('Indirizzo', validators=[Length(max=200)])
    city = StringField('Città', validators=[Length(max=100)])
    postal_code = StringField('CAP', validators=[Length(max=20)])
    country = StringField('Paese', validators=[Length(max=50)])
    submit = SubmitField('Salva Modifiche')
