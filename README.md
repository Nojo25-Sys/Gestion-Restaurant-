# 🍽️ Restaurant Management System

Une application web complète de gestion de restaurant développée avec Django, conçue pour gérer efficacement les opérations quotidiennes d'un restaurant.

## 📋 Table des matières

- [🎯 Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Technologies utilisées](#️-technologies-utilisées)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [👤 Comptes utilisateurs](#-comptes-utilisateurs)
- [📊 Modules](#-modules)
- [🔧 Développement](#-développement)
- [📝 API](#-api)
- [🧪 Tests](#-tests)
- [🚀 Déploiement](#-déploiement)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)

## 🎯 Fonctionnalités

### 📈 Statistiques et Dashboard
- **Dashboard principal** avec indicateurs clés (CA, commandes, produits)
- **Graphiques interactifs** avec Chart.js
- **Filtres temporels** (jour, semaine, mois, année)
- **Export des données** en CSV/Excel
- **Statistiques détaillées** par produits, catégories, clients

### 🍕 Gestion des Produits
- **CRUD complet** pour les produits et catégories
- **Upload d'images** avec redimensionnement automatique
- **Gestion des stocks** en temps réel
- **Alertes de stock** bas
- **Recherche et filtrage** avancés
- **Prix et marges** automatiques

### 📦 Gestion des Stocks
- **Suivi des mouvements** (entrées/sorties)
- **Historique détaillé** des transactions
- **Alertes automatiques** de réapprovisionnement
- **Rapports d'inventaire**
- **Gestion multi-dépôts**

### 🛒 Gestion des Commandes
- **Prise de commande** intuitive
- **Suivi des statuts** en temps réel
- **Historique des commandes** clients
- **Calcul automatique** des totaux
- **Gestion des annulations** et remboursements

### 👥 Gestion des Utilisateurs
- **Système de rôles** (Admin, Manager, Staff, Client)
- **Permissions granulaires**
- **Authentification sécurisée**
- **Profils utilisateurs**
- **Journal des activités**

### 🔧 Administration
- **Interface admin** Django complète
- **Configuration système**
- **Gestion des permissions**
- **Sauvegardes automatiques**
- **Logs détaillés**

## 🏗️ Architecture

```
restaurant_management/
├── 📁 apps/
│   ├── 📁 users/           # Gestion utilisateurs
│   ├── 📁 produits_app/     # Produits & catégories
│   ├── 📁 commandes_app/    # Commandes
│   ├── 📁 stock_app/       # Gestion stocks
│   └── 📁 stats_app/       # Statistiques & rapports
├── 📁 templates/           # Templates HTML
├── 📁 static/             # Fichiers statiques
├── 📁 media/              # Images uploadées
├── 📁 restaurant_management/ # Configuration Django
└── 📁 tests/              # Tests unitaires
```

## 🛠️ Technologies utilisées

### Backend
- **Django 4.2+** - Framework web principal
- **Python 3.8+** - Langage de programmation
- **SQLite** - Base de données (développement)
- **PostgreSQL** - Base de données (production)

### Frontend
- **Bootstrap 5** - Framework CSS
- **AdminLTE 3** - Template d'administration
- **Chart.js** - Graphiques interactifs
- **Font Awesome** - Icônes
- **jQuery** - Manipulation DOM

### DevOps
- **Docker** - Conteneurisation
- **Git** - Version control
- **GitHub** - Hébergement code

## 🚀 Installation

### Prérequis
```bash
# Python 3.8+
python --version

# pip (gestionnaire paquets)
pip --version

# Git
git --version
```

### Installation locale
```bash
# 1. Cloner le repository
git clone https://github.com/Nojo25-Sys/Gestion-Restaurant-.git
cd Gestion-Restaurant-

# 2. Créer environnement virtuel
python -m venv venv

# 3. Activer environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Installer dépendances
pip install -r requirements.txt

# 5. Appliquer migrations
python manage.py makemigrations
python manage.py migrate

# 6. Créer superutilisateur
python manage.py createsuperuser

# 7. Lancer serveur
python manage.py runserver
```

### Installation avec Docker
```bash
# 1. Cloner le repository
git clone https://github.com/Nojo25-Sys/Gestion-Restaurant-.git
cd Gestion-Restaurant-

# 2. Lancer avec Docker Compose
docker-compose up -d

# 3. Accéder à l'application
# http://localhost:8000
```

## ⚙️ Configuration

### Variables d'environnement
```bash
# .env
DEBUG=True
SECRET_KEY=votre-cle-secrete
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuration base de données
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'restaurant_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 👤 Comptes utilisateurs

### Compte Admin par défaut
- **Username:** `Nojo75`
- **Password:** `RestoNojo2560akn#`
- **Rôle:** Administrateur

### Types de rôles
1. **ADMIN** - Accès complet à toutes les fonctionnalités
2. **MANAGER** - Gestion produits, commandes, stocks
3. **STAFF** - Prise de commandes, consultation
4. **CLIENT** - Consultation menu, commandes

## 📊 Modules détaillés

### 📈 Module Statistiques
```python
# Vues principales
- dashboard_stats()     # Dashboard principal
- produits_stats()      # Stats produits
- commandes_stats()     # Stats commandes
- chiffre_affaires()    # CA détaillé
- export_ca()          # Export données
```

### 🍕 Module Produits
```python
# Fonctionnalités
- CRUD produits/catégories
- Upload images
- Gestion stocks
- Recherche/filtrage
- Alertes stock bas
```

### 📦 Module Stock
```python
# Mouvements
- MouvementStock model
- Historique automatique
- Alertes seuils
- Rapports inventaire
```

### 🛒 Module Commandes
```python
# Gestion
- Commande model
- LigneCommande model
- Suivi statuts
- Historique client
```

## 🔧 Développement

### Structure des vues
```python
@login_required
def vue_exemple(request):
    """
    Description de la vue
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    # Logique métier
    context = {'data': data}
    return render(request, 'template.html', context)
```

### Middlewares personnalisés
```python
# TimingMiddleware
- Mesure temps de réponse

# RateLimitMiddleware  
- Limite requêtes par utilisateur

# AuthAccessMiddleware
- Contrôle accès par rôle
```

### Templates
- **Base:** `base.html` avec sidebar navigation
- **AdminLTE:** Design responsive et moderne
- **Chart.js:** Graphiques interactifs
- **Messages:** Notifications Django intégrées

## 📝 API

### Endpoints REST
```python
# Produits
GET    /api/produits/          # Lister produits
POST   /api/produits/          # Créer produit
GET    /api/produits/{id}/      # Détail produit
PUT    /api/produits/{id}/      # Modifier produit
DELETE /api/produits/{id}/      # Supprimer produit

# Commandes
GET    /api/commandes/         # Lister commandes
POST   /api/commandes/         # Créer commande
GET    /api/commandes/{id}/     # Détail commande
PUT    /api/commandes/{id}/     # Modifier statut

# Statistiques
GET    /api/stats/dashboard/     # Dashboard
GET    /api/stats/ca/           # Chiffre d'affaires
GET    /api/stats/produits/     # Stats produits
```

### Format réponses
```json
{
    "success": true,
    "data": {...},
    "message": "Opération réussie",
    "count": 10
}
```

## 🧪 Tests

### Lancer les tests
```bash
# Tous les tests
python manage.py test

# Tests par module
python manage.py test users
python manage.py test produits_app
python manage.py test commandes_app
python manage.py test stock_app
python manage.py test stats_app

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
```

### Tests disponibles
- **Tests unitaires** pour tous les modèles
- **Tests d'intégration** pour les vues
- **Tests fonctionnels** pour les workflows
- **Tests API** pour les endpoints REST

## 🚀 Déploiement

### Production avec Docker
```bash
# 1. Configuration production
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com

# 2. Build et déploiement
docker-compose -f docker-compose.prod.yml up -d

# 3. Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Déploiement manuel
```bash
# 1. Serveur web (Nginx/Apache)
# 2. WSGI (Gunicorn/uWSGI)
# 3. Base de données PostgreSQL
# 4. Fichiers statiques
# 5. Variables environnement
```

### Monitoring
- **Logs Django** pour erreurs
- **Metrics** performance
- **Alertes** stock bas
- **Sauvegardes** automatiques

## 🤝 Contribution

### Comment contribuer
1. **Forker** le repository
2. **Créer branche** feature/nom-fonctionnalité
3. **Développer** avec tests
4. **Commiter** avec messages clairs
5. **Pusher** vers fork
6. **Pull request** vers main

### Standards de code
```python
# Style PEP 8
# Docstrings pour fonctions
# Tests unitaires obligatoires
# Comments explicatifs
```

### Messages de commit
```
feat: nouvelle fonctionnalité
fix: correction bug
docs: mise à jour documentation
refactor: refactoring code
test: ajout tests
```

## 📄 Licence

Ce projet est sous licence **MIT** - voir fichier [LICENSE](LICENSE) pour détails.

## 📞 Contact

- **Développeur:** Nojo25-Sys
- **Email:** contact@restaurant-management.com
- **GitHub:** [@Nojo25-Sys](https://github.com/Nojo25-Sys)

---

## 🎯 Roadmap

### Version 2.0 (En développement)
- [ ] **API REST complète** avec Django REST Framework
- [ ] **Application mobile** React Native
- [ ] **Notifications** temps réel WebSocket
- [ ] **Paiements en ligne** Stripe/PayPal
- [ ] **Livraison tracking** GPS
- [ ] **Multi-restaurants** support

### Version 1.5 (Prochainement)
- [ ] **Rapports avancés** PDF/Excel
- [ ] **Planning employés** 
- [ ] **Gestion fournisseurs**
- [ ] **Menu digital** QR code
- [ ] **Loyalty program**

### Version 1.1 (Correctifs)
- [ ] **Optimisation** performance
- [ ] **Tests automatisés** CI/CD
- [ ] **Documentation** API complète
- [ ] **Accessibilité** WCAG 2.0

---

**⭐ Merci d'avoir utilisé Restaurant Management System!**

Si ce projet vous a été utile, n'hésitez pas à:
- Laisser une ⭐ sur GitHub
- Reporter des 🐛 issues
- Suggérer des 💡 améliorations
- Contribuer au 🚀 développement
