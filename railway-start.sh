#!/bin/bash

# Script de démarrage pour Railway
echo "Démarrage de l'application Django sur Railway..."

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate --noinput

# Créer un superutilisateur si nécessaire
python manage.py shell << EOF
from users.models import User
if not User.objects.filter(username='Nojo75').exists():
    User.objects.create_superuser(
        username='Nojo75',
        password='RestoNojo2560akn#',
        email='admin@restaurant-management.com',
        first_name='Admin',
        last_name='System',
        role='ADMIN'
    )
    print("Superutilisateur créé")
else:
    print("Superutilisateur existe déjà")
EOF

# Démarrer l'application
echo "Lancement de Gunicorn..."
gunicorn restaurant_management.wsgi:application --bind 0.0.0.0:$PORT --workers 3
