from pathlib import Path
from decouple import config, Csv
from django.contrib.messages import constants as msg_constants
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY    = config('SECRET_KEY')
DEBUG         = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE    = config('CSRF_COOKIE_SECURE',    default=not DEBUG, cast=bool)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users', 'produits_app', 'stock_app', 'commandes_app', 'stats_app',
    'crispy_forms', 'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

ROOT_URLCONF        = 'restaurant_management.urls'
AUTH_USER_MODEL     = 'users.User'
LOGIN_URL           = 'users:login'
LOGOUT_REDIRECT_URL = 'users:login'
LOGIN_REDIRECT_URL  = 'users:dashboard'

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

WSGI_APPLICATION = 'restaurant_management.wsgi.application'

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

CACHES = {
    'default': {
        'BACKEND':  config('CACHE_BACKEND',  default='django.core.cache.backends.filebased.FileBasedCache'),
        'LOCATION': config('CACHE_LOCATION', default=str(BASE_DIR / '.cache')),
        'TIMEOUT':  300,
    }
}

RATE_LIMIT_REQUESTS = config('RATE_LIMIT_REQUESTS', default=5,  cast=int)
RATE_LIMIT_WINDOW   = config('RATE_LIMIT_WINDOW',   default=60, cast=int)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Dakar'
USE_I18N      = True
USE_TZ        = True

STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'
MEDIA_URL        = '/media/'
MEDIA_ROOT       = BASE_DIR / 'media'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'

MESSAGE_TAGS = {
    msg_constants.DEBUG:   'debug',
    msg_constants.INFO:    'info',
    msg_constants.SUCCESS: 'success',
    msg_constants.WARNING: 'warning',
    msg_constants.ERROR:   'danger',
}

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
    'root': {'handlers': ['console'], 'level': config('LOG_LEVEL', default='INFO')},
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'WARNING', 'propagate': False},
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Railway Configuration
import dj_database_url
import os

# Database configuration for Railway
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }

# Static files configuration for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration for production
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True