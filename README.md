# Template E-commerce Flask Riutilizzabile

Un template completo e modulare per creare rapidamente siti e-commerce con Flask. Progettato per essere facilmente personalizzabile e riutilizzabile per ogni progetto.

## 🚀 Caratteristiche

### Funzionalità Core
- ✅ **Autenticazione completa** (login, registrazione, profilo utente)
- ✅ **Catalogo prodotti** con categorie, ricerca e filtri
- ✅ **Carrello della spesa** con gestione quantità
- ✅ **Sistema di checkout** con calcolo IVA e spese di spedizione
- ✅ **Gestione ordini** per utenti e amministratori
- ✅ **Pannello admin** per gestire prodotti, ordini e utenti

### Architettura
- 🏗️ **Blueprint modulari** per una facile manutenzione
- 🗄️ **SQLAlchemy ORM** con supporto SQLite, PostgreSQL, MySQL
- 🔐 **Flask-Login** per gestione sessioni sicure
- 📝 **Flask-WTF** per form validation
- 🎨 **Bootstrap 5** per design responsive
- 🔄 **Flask-Migrate** per migrazioni database

## 📁 Struttura Progetto

```
Ecommerce_replicabile/
├── app/
│   ├── __init__.py              # Factory pattern Flask
│   ├── models/                  # Modelli database
│   │   ├── user.py             # Utenti e autenticazione
│   │   ├── product.py          # Prodotti e categorie
│   │   ├── cart.py             # Carrello
│   │   └── order.py            # Ordini
│   ├── auth/                    # Blueprint autenticazione
│   ├── shop/                    # Blueprint negozio
│   ├── cart/                    # Blueprint carrello
│   ├── admin/                   # Blueprint amministrazione
│   ├── templates/               # Template Jinja2
│   ├── static/                  # CSS, JS, immagini
│   └── utils/                   # Utilities e decorators
├── config.py                    # Configurazioni
├── requirements.txt             # Dipendenze Python
├── run.py                      # Entry point applicazione
└── README.md                   # Questa documentazione
```

## 🛠️ Installazione

### 1. Clona o copia il template

```bash
# Se usi git
git clone <repository-url>
cd Ecommerce_replicabile

# Oppure copia semplicemente la cartella
```

### 2. Crea ambiente virtuale

```bash
python -m venv venv

# Attiva l'ambiente virtuale
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Installa dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura variabili d'ambiente

```bash
# Copia il file di esempio
cp .env.example .env

# Modifica .env con le tue configurazioni
```

### 5. Inizializza il database

```bash
# Opzione 1: Auto-creazione al primo avvio (SQLite)
python run.py

# Opzione 2: Usa Flask-Migrate per migrazioni
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Crea un utente admin (opzionale)

Apri una shell Python:

```python
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(
        username='admin',
        email='admin@example.com',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
```

## 🎯 Come Personalizzare per Ogni Progetto

### 1. Configurazione Base (`config.py`)

```python
# Modifica questi valori in config.py:
PROJECT_NAME = "Il Mio E-commerce"  # Nome del tuo negozio
TAX_RATE = 0.22                     # Tasso IVA
SHIPPING_COST = 5.00                # Costo spedizione
FREE_SHIPPING_THRESHOLD = 50.00     # Soglia spedizione gratis
CURRENCY = 'EUR'                    # Valuta
CURRENCY_SYMBOL = '€'               # Simbolo valuta
```

### 2. Stili e Design (`app/static/css/style.css`)

```css
/* Personalizza i colori nel file CSS */
:root {
    --primary-color: #007bff;    /* Colore primario */
    --secondary-color: #6c757d;  /* Colore secondario */
}
```

### 3. Template (`app/templates/`)

Modifica i template HTML per adattarli al tuo brand:
- `base.html` - Layout principale e navbar
- `shop/index.html` - Homepage
- Footer in `base.html`

### 4. Immagini e Loghi

Sostituisci le immagini in `app/static/images/` con:
- Logo del tuo brand
- Immagini prodotti
- Banner homepage

## 🚀 Avvio Applicazione

### Development

```bash
python run.py
```

Visita: `http://localhost:5000`

### Production

```bash
# Imposta variabili d'ambiente
export FLASK_ENV=production
export SECRET_KEY="your-super-secret-key"

# Avvia con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

## 📊 Gestione Database

### Aggiungere Prodotti e Categorie

#### Via Python Shell

```python
from app import create_app, db
from app.models.product import Product, Category

app = create_app()
with app.app_context():
    # Crea categoria
    cat = Category(name='Elettronica', slug='elettronica')
    db.session.add(cat)
    db.session.commit()

    # Crea prodotto
    prod = Product(
        name='Smartphone XYZ',
        slug='smartphone-xyz',
        price=599.99,
        stock=10,
        category_id=cat.id,
        is_active=True
    )
    db.session.add(prod)
    db.session.commit()
```

#### Via Pannello Admin

1. Accedi come admin: `/admin`
2. Vai su "Prodotti" > "Aggiungi Prodotto"
3. Compila il form e salva

## 🔐 Sicurezza

### Checklist Prima di Andare in Produzione

- [ ] Cambia `SECRET_KEY` in produzione
- [ ] Usa database PostgreSQL/MySQL invece di SQLite
- [ ] Abilita HTTPS
- [ ] Configura CORS se necessario
- [ ] Limita tentativi di login
- [ ] Backup regolari del database
- [ ] Valida sempre input utente
- [ ] Sanitizza upload file

## 📦 Componenti Disponibili

### Modelli Database

- **User**: Gestione utenti e autenticazione
- **Product**: Prodotti del catalogo
- **Category**: Categorie prodotti
- **Cart**: Carrello acquisti
- **Order**: Ordini completati
- **OrderItem**: Dettagli item ordini

### Blueprint

- **auth**: Login, registrazione, profilo
- **shop**: Catalogo, prodotti, categorie
- **cart**: Carrello e checkout
- **admin**: Pannello amministrazione

## 🎨 Template Disponibili

### Shop
- `shop/index.html` - Homepage
- `shop/products.html` - Catalogo con filtri
- `shop/product_detail.html` - Dettaglio prodotto
- `shop/category.html` - Prodotti per categoria

### Auth
- `auth/login.html` - Login
- `auth/register.html` - Registrazione
- `auth/profile.html` - Profilo utente
- `auth/orders.html` - Storico ordini

### Cart
- `cart/view.html` - Visualizza carrello
- `cart/checkout.html` - Checkout
- `cart/order_confirmation.html` - Conferma ordine

### Admin
- `admin/dashboard.html` - Dashboard
- `admin/products.html` - Gestione prodotti
- `admin/orders.html` - Gestione ordini
- `admin/order_detail.html` - Dettaglio ordine

## 🔧 Estensioni Future

Puoi facilmente aggiungere:

- 💳 **Pagamenti Stripe/PayPal**: Integra gateway pagamento
- 📧 **Email notifiche**: Conferme ordine via email
- 🖼️ **Upload immagini**: Sistema upload multiplo
- ⭐ **Recensioni prodotti**: Sistema rating e review
- 🏷️ **Coupon e sconti**: Codici sconto
- 📊 **Analytics**: Statistiche vendite
- 🔍 **SEO**: Meta tags e sitemap
- 🌍 **Multi-lingua**: i18n support
- 📱 **API REST**: Per app mobile

## 📝 Workflow Consigliato

### Per Ogni Nuovo Progetto E-commerce:

1. **Copia template** in nuova directory
2. **Rinomina progetto** in `config.py`
3. **Personalizza colori** in CSS
4. **Modifica template** base e footer
5. **Aggiungi logo** e immagini
6. **Configura database** produzione
7. **Popola categorie** e prodotti
8. **Testa checkout** completo
9. **Deploy** su server

## 🐛 Troubleshooting

### Database locked
Se usi SQLite in produzione, considera PostgreSQL/MySQL

### Import errors
Assicurati che l'ambiente virtuale sia attivato

### Template not found
Verifica la struttura delle cartelle template

### Static files non caricano
Controlla i permessi della cartella static

## 📄 Licenza

Questo template è libero da usare per progetti personali e commerciali.

## 🤝 Contributi

Sentiti libero di migliorare questo template e condividere le modifiche!

## 📧 Supporto

Per domande o problemi, consulta la documentazione Flask ufficiale:
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap](https://getbootstrap.com/)

---

**Creato con ❤️ per semplificare lo sviluppo di e-commerce**