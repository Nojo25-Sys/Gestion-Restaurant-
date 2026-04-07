# Déploiement sur Railway - Étapes Complètes

## 1. Préparation du projet

### Créer requirements.txt
```bash
pip freeze > requirements.txt
```

### Créer Procfile
```web: gunicorn restaurant_management.wsgi:application --bind 0.0.0.0:$PORT```

### Créer .env
```
DEBUG=False
SECRET_KEY=votre-cle-secrete-railway
ALLOWED_HOSTS=railway.app,localhost
DATABASE_URL=postgresql://username:password@host:port/dbname
```

## 2. Configuration Django

### settings.py modifications
```python
import os
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = 'mediafiles'
MEDIA_URL = '/media/'

# Security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

## 3. Déploiement Railway

### Étapes:
1. **Créer compte Railway** - railway.app
2. **Connecter GitHub** - Importer repository
3. **Configurer variables environnement**
4. **Définir commande de démarrage**
5. **Activer PostgreSQL addon**
6. **Déployer**

### Commandes Railway:
```bash
# Installer CLI
npm install -g @railway/cli

# Se connecter
railway login

# Initialiser projet
railway init

# Ajouter PostgreSQL
railway add postgresql

# Déployer
railway up
```

## 4. Variables d'environnement Railway

Dans dashboard Railway > Settings > Variables:
```
DEBUG=False
SECRET_KEY=generer-cle-aleatoire
ALLOWED_HOSTS=votre-app.railway.app
PYTHON_VERSION=3.11
```

## 5. Finalisation

### Collecter static files
```bash
# Ajouter dans settings.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Installer whitenoise
pip install whitenoise
```

### Lancer déploiement final
```bash
git add .
git commit -m "deploy: ready for railway"
git push
```

## 6. Accès application

- **URL:** `https://votre-app.railway.app`
- **Admin:** `https://votre-app.railway.app/admin`
- **Database:** Railway dashboard > PostgreSQL
