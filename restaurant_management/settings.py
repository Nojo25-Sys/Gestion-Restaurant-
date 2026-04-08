from pathlib import Path
from decouple import config, Csv
from django.contrib.messages import constants as msg_constants
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Sécurité ────────────────────────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG       = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost,.railway.app',
    cast=Csv()
)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://*.railway.app',
    cast=Csv()
)

# ─── Applications ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'users',
    'produits_app',
    'stock_app',
    'commandes_app',
    'stats_app',
    'crispy_forms',
    'crispy_bootstrap5',
]

# ─── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',           # juste après SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'restaurant_management.middleware.TimingMiddleware',
    'restaurant_management.middleware.RateLimitMiddleware',
    'restaurant_management.middleware.AuthAccessMiddleware',
]

# ─── URLs / Auth ───────────────────────────────────────────────────────────────
ROOT_URLCONF        = 'restaurant_management.urls'
WSGI_APPLICATION    = 'restaurant_management.wsgi.application'
AUTH_USER_MODEL     = 'users.User'
LOGIN_URL           = 'users:login'
LOGOUT_REDIRECT_URL = 'users:login'
LOGIN_REDIRECT_URL  = 'users:dashboard'

# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

# ─── Base de données ──────────────────────────────────────────────────────────
# Priorité à DATABASE_URL (Railway PostgreSQL), sinon fallback SQLite en dev
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=60,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':       config('DB_ENGINE',   default='django.db.backends.sqlite3'),
            'NAME':         config('DB_NAME',     default=str(BASE_DIR / 'db.sqlite3')),
            'USER':         config('DB_USER',     default=''),
            'PASSWORD':     config('DB_PASSWORD', default=''),
            'HOST':         config('DB_HOST',     default=''),
            'PORT':         config('DB_PORT',     default=''),
            'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=60, cast=int),
        }
    }

# ─── Cache ────────────────────────────────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND':  config('CACHE_BACKEND',  default='django.core.cache.backends.filebased.FileBasedCache'),
        'LOCATION': config('CACHE_LOCATION', default=str(BASE_DIR / '.cache')),
        'TIMEOUT':  300,
    }
}

# ─── Rate limiting ────────────────────────────────────────────────────────────
RATE_LIMIT_REQUESTS = config('RATE_LIMIT_REQUESTS', default=5,  cast=int)
RATE_LIMIT_WINDOW   = config('RATE_LIMIT_WINDOW',   default=60, cast=int)

# ─── Mots de passe ────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalisation ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Dakar'
USE_I18N      = True
USE_TZ        = True

# ─── Fichiers statiques & media ───────────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# ─── Crispy Forms ─────────────────────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'

# ─── Messages ─────────────────────────────────────────────────────────────────
MESSAGE_TAGS = {
    msg_constants.DEBUG:   'debug',
    msg_constants.INFO:    'info',
    msg_constants.SUCCESS: 'success',
    msg_constants.WARNING: 'warning',
    msg_constants.ERROR:   'danger',
}

# ─── Logging ──────────────────────────────────────────────────────────────────
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} — {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class':       'logging.handlers.RotatingFileHandler',
            'filename':    BASE_DIR / 'logs' / 'restaurant.log',
            'maxBytes':    10 * 1024 * 1024,
            'backupCount': 5,
            'formatter':   'verbose',
        },
    },
    'root':    {'handlers': ['console'], 'level': config('LOG_LEVEL', default='INFO')},
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'WARNING', 'propagate': False},
    },
}

# ─── Sécurité en production ───────────────────────────────────────────────────
if not DEBUG:
    SECURE_SSL_REDIRECT          = True
    SECURE_PROXY_SSL_HEADER      = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS          = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF  = True
    SESSION_COOKIE_SECURE        = True
    CSRF_COOKIE_SECURE           = True
    X_FRAME_OPTIONS              = 'DENY'

# ─── Divers ───────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
