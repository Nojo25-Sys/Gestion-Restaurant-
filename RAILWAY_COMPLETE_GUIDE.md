# 🚀 DÉPLOIEMENT RAILWAY - GUIDE COMPLET

## ÉTAPE 1: PRÉPARATION COMPTE RAILWAY

### 1.1 Créer compte Railway
```bash
# 1. Allez sur https://railway.app
# 2. Cliquez "Sign up" ou "Login with GitHub"
# 3. Autorisez l'accès à votre compte GitHub
# 4. Choisissez votre plan (Free pour commencer)
```

### 1.2 Vérifier prérequis
```bash
# Assurez-vous que:
✅ Repository GitHub est public
✅ requirements.txt contient toutes les dépendances
✅ Procfile est présent
✅ settings.py configuré pour production
```

## ÉTAPE 2: IMPORTATION DU PROJET

### 2.1 Depuis le dashboard Railway
```bash
# 1. Cliquez "New Project"
# 2. Choisissez "Deploy from GitHub repo"
# 3. Sélectionnez "Gestion-Restaurant-"
# 4. Cliquez "Deploy Now"
# 5. Attendez le déploiement automatique
```

### 2.2 Alternative avec CLI Railway
```bash
# Installer Railway CLI
npm install -g @railway/cli

# Se connecter
railway login

# Importer le projet
railway import https://github.com/Nojo25-Sys/Gestion-Restaurant-
```

## ÉTAPE 3: CONFIGURATION BASE DE DONNÉES

### 3.1 Ajouter PostgreSQL
```bash
# Dans le dashboard Railway:
# 1. Cliquez sur votre projet
# 2. "New Service" → "Add Service"
# 3. Choisissez "PostgreSQL"
# 4. Cliquez "Add PostgreSQL"
```

### 3.2 Vérifier DATABASE_URL
```bash
# Railway génère automatiquement:
DATABASE_URL=postgresql://username:password@host:port/dbname

# Cette variable sera disponible dans:
# Settings → Variables d'environnement
```

## ÉTAPE 4: CONFIGURATION VARIABLES D'ENVIRONNEMENT

### 4.1 Variables requises
Dans Railway dashboard → Settings → Variables:

```bash
# Variables essentielles:
DEBUG=False
SECRET_KEY=votre-cle-secrete-aleatoire-ici
ALLOWED_HOSTS=votre-app.railway.app,railway.app
PYTHON_VERSION=3.11

# Optionnelles:
DJANGO_SETTINGS_MODULE=restaurant_management.settings
```

### 4.2 Générer SECRET_KEY
```bash
# Générez une clé secrète:
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Copiez la clé générée dans les variables Railway
```

## ÉTAPE 5: DÉPLOIEMENT AUTOMATIQUE

### 5.1 Processus Railway
```bash
# Railway exécute automatiquement:
# 1. git clone (déjà fait)
# 2. pip install -r requirements.txt
# 3. python manage.py collectstatic --noinput
# 4. Démarrer gunicorn via Procfile
# 5. Exposer l'application sur Internet
```

### 5.2 Vérifier le déploiement
```bash
# Dans Railway dashboard:
# 1. Onglet "Logs" pour voir les erreurs
# 2. Onglet "Metrics" pour monitoring
# 3. Onglet "Settings" pour configuration
```

## ÉTAPE 6: ACCÈS À L'APPLICATION

### 6.1 URLs après déploiement
```bash
# URL principale:
https://votre-nom-projet.railway.app

# URL admin Django:
https://votre-nom-projet.railway.app/admin

# URL API (si implémentée):
https://votre-nom-projet.railway.app/api/
```

### 6.2 Première connexion
```bash
# 1. Accédez à l'URL principale
# 2. Cliquez "Connexion"
# 3. Utilisez le compte admin:
   Username: Nojo75
   Password: RestoNojo2560akn#
# 4. Vérifiez que tout fonctionne
```

## ÉTAPE 7: CONFIGURATION POST-DÉPLOIEMENT

### 7.1 Créer superutilisateur en production
```bash
# Option 1: Via Railway shell
railway open shell
python manage.py createsuperuser

# Option 2: Via admin existant
# Le compte Nojo75 est déjà configuré comme superadmin
```

### 7.2 Vérifier les médias
```bash
# Les fichiers uploadés seront dans:
# /mediafiles/ (configuré dans settings.py)

# Pour accéder aux médias:
# Configurez STATIC_URL et MEDIA_URL correctement
```

## ÉTAPE 8: MONITORING ET MAINTENANCE

### 8.1 Logs Railway
```bash
# Pour voir les logs en temps réel:
railway logs

# Pour voir les logs d'un service spécifique:
railway logs <service-name>
```

### 8.2 Mises à jour
```bash
# Pour mettre à jour l'application:
git add .
git commit -m "update: nouvelle fonctionnalité"
git push

# Railway détecte automatiquement le push et redéploie
```

## ÉTAPE 9: DÉPANNAGE

### 9.1 Problèmes communs
```bash
❌ Erreur 500: Vérifiez les logs Railway
❌ Erreur database: Vérifiez DATABASE_URL
❌ Erreur static: Vérifiez collectstatic
❌ Erreur permission: Vérifiez ALLOWED_HOSTS
```

### 9.2 Commandes utiles
```bash
# Redémarrer un service:
railway restart <service-name>

# Voir les variables:
railway variables

# Ouvrir un shell:
railway open shell

# Voir le statut:
railway status
```

## ÉTAPE 10: SÉCURITÉ

### 10.1 HTTPS obligatoire
```bash
# Railway force HTTPS automatiquement:
✅ SECURE_SSL_REDIRECT = True
✅ SESSION_COOKIE_SECURE = True
✅ CSRF_COOKIE_SECURE = True
```

### 10.2 Variables sensibles
```bash
# Ne jamais exposer:
❌ SECRET_KEY dans le code
❌ DATABASE_URL dans le code public
❌ Mots de passe en clair

# Utilisez toujours:
✅ Variables d'environnement Railway
✅ Django settings avec os.environ.get()
```

## RÉSUMÉ RAPIDE

### Commandes une par une:
```bash
# 1. railway login
# 2. railway import https://github.com/Nojo25-Sys/Gestion-Restaurant-
# 3. railway add postgresql
# 4. railway variables (configurer DEBUG=False, SECRET_KEY, ALLOWED_HOSTS)
# 5. railway up
```

### Temps estimé: 10-15 minutes

---

## 🎯 RÉSULTAT FINAL

Après ces étapes, votre application sera accessible:
- **URL:** `https://votre-app.railway.app`
- **Admin:** `https://votre-app.railway.app/admin`
- **Base de données:** PostgreSQL gérée par Railway
- **Fichiers statiques:** Servis automatiquement
- **Monitoring:** Disponible dans dashboard Railway

## 📞 SUPPORT

- **Documentation Railway:** https://docs.railway.app/
- **Support:** https://railway.app/support
- **Status:** https://status.railway.app/

---

**🚀 Votre projet Restaurant Management est maintenant prêt pour la production!**
