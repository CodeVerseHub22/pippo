# 🚀 Portfolio - Web & Mobile Developer

Un sito portfolio professionale costruito con Django, Bootstrap 5 e SQLite, con un'area admin completa per gestire contenuti e palette di colori.

## ✨ Caratteristiche

- 🎨 **Palette Colori Dinamiche** - Cambia i colori del sito dall'admin senza modificare codice
- 📱 **Design Responsive** - Mobile-first approach con Bootstrap 5
- 🌙 **Dark Mode** - Toggle per tema chiaro/scuro
- 📂 **Gestione Progetti** - CRUD completo con categorie e filtri
- 💼 **Timeline Esperienze** - Visualizzazione cronologica del percorso lavorativo
- 🛠️ **Skills con Livelli** - Barre di progresso e stelline
- 📧 **Form Contatti** - Con validazione e salvataggio messaggi
- 🔐 **Admin Personalizzato** - Interfaccia intuitiva per gestire tutto

## 📋 Requisiti

- Python 3.10+
- pip (Python package manager)

## 🛠️ Installazione

### 1. Clona o accedi alla cartella del progetto

```powershell
cd c:\Users\Postazione16Aula1\Desktop\Portfolio\portfolio_project
```

### 2. Crea un ambiente virtuale

```powershell
python -m venv venv
```

### 3. Attiva l'ambiente virtuale

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Installa le dipendenze

```powershell
pip install -r requirements.txt
```

### 5. Esegui le migrazioni del database

```powershell
python manage.py makemigrations portfolio
python manage.py migrate
```

### 6. Crea un superuser per l'admin

```powershell
python manage.py createsuperuser
```

Inserisci username, email e password quando richiesto.

### 7. Avvia il server di sviluppo

```powershell
python manage.py runserver
```

### 8. Accedi al sito

- **Sito**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## 📁 Struttura del Progetto

```
portfolio_project/
├── manage.py                    # Script gestione Django
├── requirements.txt             # Dipendenze Python
├── db.sqlite3                   # Database (creato dopo migrate)
├── portfolio_project/           # Configurazione progetto
│   ├── settings.py             # Impostazioni Django
│   ├── urls.py                 # URL routing principale
│   └── ...
├── portfolio/                   # App principale
│   ├── models.py               # Modelli database
│   ├── views.py                # Logic delle pagine
│   ├── admin.py                # Configurazione admin
│   ├── forms.py                # Form contatti
│   ├── urls.py                 # URL routing app
│   ├── templates/              # Template HTML
│   │   ├── base.html           # Template base
│   │   ├── home.html           # Home page
│   │   ├── projects.html       # Lista progetti
│   │   ├── project_detail.html # Dettagli progetto
│   │   ├── about.html          # Chi sono
│   │   ├── contact.html        # Contatti
│   │   └── success.html        # Conferma invio
│   └── static/                 # File statici
│       ├── css/
│       │   ├── style.css       # Stili principali
│       │   └── theme.css       # Variabili colori
│       └── js/
│           └── script.js       # JavaScript
└── media/                      # Upload immagini
```

## 🎨 Personalizzazione

### Dall'Admin Panel

1. **Impostazioni Sito** (`/admin/portfolio/sitesettings/`)
   - Nome e bio autore
   - Email e contatti
   - Link social (GitHub, LinkedIn, etc.)
   - Foto profilo

2. **Palette Colori** (`/admin/portfolio/colorpalette/`)
   - Crea palette personalizzate
   - Attiva la palette desiderata
   - I colori vengono applicati automaticamente

3. **Progetti** (`/admin/portfolio/project/`)
   - Aggiungi nuovi progetti
   - Imposta come "In Evidenza" per mostrarli in home
   - Ordina trascinando

4. **Skills** (`/admin/portfolio/skill/`)
   - Aggiungi competenze
   - Imposta livello (1-5 stelle)
   - Scegli icona FontAwesome

5. **Esperienze** (`/admin/portfolio/experience/`)
   - Aggiungi esperienze lavorative
   - Gestisci ordine cronologico

## 📧 Configurazione Email (Produzione)

Per inviare email reali, modifica `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tua@email.com'
EMAIL_HOST_PASSWORD = 'password_app'
```

## 🔒 Sicurezza per Produzione

Prima del deploy, modifica `settings.py`:

```python
DEBUG = False
SECRET_KEY = 'chiave-segreta-sicura'
ALLOWED_HOSTS = ['tuodominio.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🌐 API Endpoints

- `GET /api/palette/` - Restituisce la palette colori attiva (JSON)
- `GET /api/skills/` - Restituisce tutte le skill (JSON)

## 🚀 Deploy

### Heroku

1. Installa `gunicorn` e `whitenoise`
2. Crea `Procfile`:
   ```
   web: gunicorn portfolio_project.wsgi
   ```
3. Configura le variabili d'ambiente

### PythonAnywhere

1. Carica i file
2. Configura il virtualenv
3. Imposta il WSGI

## 📝 Licenza

Questo progetto è open source. Sentiti libero di usarlo e modificarlo.

## 👨‍💻 Autore

Creato con ❤️ per il tuo portfolio professionale.

---

**Buon sviluppo!** 🎉
