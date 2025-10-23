# Configuration PythonAnywhere pour ETRAGC SARLU

## 📋 Informations de connexion MySQL

**Adresse de l'hôte:** `ETRAGCSARLU.mysql.pythonanywhere-services.com`  
**Nom d'utilisateur:** `ETRAGCSARLU`  
**Nom de la base de données:** `ETRAGCSARLU$par défaut`

⚠️ **Important:** Avec un compte gratuit PythonAnywhere, vous ne pouvez vous connecter à MySQL que depuis le code exécuté sur PythonAnywhere.

## ⚙️ Configuration du fichier `.env`

### 1. Modifier votre fichier `.env`

Ajoutez ou modifiez ces lignes dans votre fichier `.env` :

```env
# Base de données MySQL PythonAnywhere
DB_ENGINE=django.db.backends.mysql
DB_NAME=ETRAGCSARLU$par défaut
DB_USER=ETRAGCSARLU
DB_PASSWORD=VOTRE_MOT_DE_PASSE_MYSQL
DB_HOST=ETRAGCSARLU.mysql.pythonanywhere-services.com
DB_PORT=3306
```

**Remplacez `VOTRE_MOT_DE_PASSE_MYSQL`** par le mot de passe MySQL que vous avez défini dans PythonAnywhere.

⚠️ **Sécurité:** Ce mot de passe doit être différent de votre mot de passe principal PythonAnywhere.

## 📦 Installation des dépendances

### 1. Installer mysqlclient

Sur PythonAnywhere, ouvrez une console Bash et exécutez :

```bash
pip install --user mysqlclient
```

**Alternative avec PyMySQL** (si mysqlclient pose problème) :

```bash
pip install --user pymysql
```

Si vous utilisez PyMySQL, ajoutez dans `config/__init__.py` :

```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 🗄️ Création et configuration de la base de données

### 1. Créer la base de données

Sur PythonAnywhere, dans l'onglet **Databases** :
- Nom de la base de données : `par défaut` (PythonAnywhere ajoutera automatiquement le préfixe `ETRAGCSARLU$`)
- Définir un mot de passe MySQL sécurisé

### 2. Appliquer les migrations

Dans la console Bash PythonAnywhere :

```bash
cd ~/ETRAGC_SARLU  # ou le nom de votre dossier projet
python manage.py migrate
```

### 3. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 4. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

## 🔄 Migration depuis SQLite vers MySQL

Si vous avez déjà des données en local avec SQLite :

### 1. Exporter les données (en local)

```powershell
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data_backup.json
```

### 2. Uploader le fichier sur PythonAnywhere

- Via l'interface Files de PythonAnywhere
- Ou via Git si vous utilisez un dépôt

### 3. Importer les données (sur PythonAnywhere)

```bash
python manage.py loaddata data_backup.json
```

## 🌐 Configuration de l'application Web

### 1. Créer une Web App

Dans l'onglet **Web** de PythonAnywhere :
- Créer une nouvelle application Web
- Choisir **Manual configuration**
- Sélectionner **Python 3.10** (ou la version que vous utilisez)

### 2. Configurer le WSGI

Modifier le fichier WSGI (exemple : `/var/www/ETRAGCSARLU_pythonanywhere_com_wsgi.py`) :

```python
import os
import sys

# Ajouter le chemin de votre projet
path = '/home/ETRAGCSARLU/ETRAGC_SARLU'
if path not in sys.path:
    sys.path.append(path)

# Définir les variables d'environnement depuis .env
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/ETRAGC_SARLU')
load_dotenv(os.path.join(project_folder, '.env'))

# Configurer Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 3. Configurer les fichiers statiques

Dans l'onglet **Web**, section **Static files** :

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/ETRAGCSARLU/ETRAGC_SARLU/staticfiles` |
| `/media/` | `/home/ETRAGCSARLU/ETRAGC_SARLU/media` |

### 4. Configurer le virtualenv (optionnel)

Si vous utilisez un environnement virtuel :
```
/home/ETRAGCSARLU/ETRAGC_SARLU/venv
```

## 🔐 Variables d'environnement

Créez un fichier `.env` sur PythonAnywhere avec :

```env
# Configuration ETRAGC SARLU
SECRET_KEY=votre-cle-secrete-unique-et-longue
DEBUG=False
ALLOWED_HOSTS=ETRAGCSARLU.pythonanywhere.com

# Base de données MySQL PythonAnywhere
DB_ENGINE=django.db.backends.mysql
DB_NAME=ETRAGCSARLU$par défaut
DB_USER=ETRAGCSARLU
DB_PASSWORD=votre_mot_de_passe_mysql
DB_HOST=ETRAGCSARLU.mysql.pythonanywhere-services.com
DB_PORT=3306

# Email (optionnel)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@etragc-sarlu.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-email

# Paramètres entreprise
COMPANY_NAME=ÉLITE DES TRAVAUX DE GÉNIE CIVIL SARLU
COMPANY_SHORT_NAME=ETRAGC SARLU
COMPANY_RCCM=GN.TCC.2024.B.02513
COMPANY_NIF=797139748
COMPANY_TVA=2X
COMPANY_EMAIL=info@etragc-sarlu.com
COMPANY_PHONE=+224 628 78 78 03
COMPANY_PHONE_2=+224 612 79 79 03
COMPANY_ADDRESS=Kankan, Quartier Missira, Guinée
COMPANY_WEBSITE=www.etragc-sarlu.com
```

## 🧪 Test de la connexion

Dans la console Bash PythonAnywhere :

```bash
python manage.py check
python manage.py dbshell
```

## 🚀 Démarrer l'application

1. Cliquez sur **Reload** dans l'onglet Web
2. Visitez votre site : `https://ETRAGCSARLU.pythonanywhere.com`

## ⚠️ Problèmes courants

### Erreur: "No module named 'MySQLdb'"
**Solution:** 
```bash
pip install --user mysqlclient
# ou
pip install --user pymysql
```

### Erreur: "Can't connect to MySQL server"
**Solution:** 
- Vérifiez que vous utilisez le bon hostname : `ETRAGCSARLU.mysql.pythonanywhere-services.com`
- Vérifiez le nom d'utilisateur : `ETRAGCSARLU`
- Vérifiez le nom de la base de données : `ETRAGCSARLU$par défaut`

### Erreur: "Access denied"
**Solution:** 
- Vérifiez votre mot de passe MySQL dans le fichier `.env`
- Réinitialisez le mot de passe MySQL dans l'onglet Databases de PythonAnywhere

### Les fichiers statiques ne se chargent pas
**Solution:**
```bash
python manage.py collectstatic --noinput
```
Et vérifiez la configuration des Static files dans l'onglet Web.

### L'application ne se recharge pas
**Solution:** Cliquez sur le bouton **Reload** dans l'onglet Web après chaque modification.

## 📝 Checklist de déploiement

- [ ] Compte PythonAnywhere créé
- [ ] Base de données MySQL créée (`ETRAGCSARLU$par défaut`)
- [ ] Mot de passe MySQL défini
- [ ] Code uploadé sur PythonAnywhere
- [ ] Fichier `.env` configuré avec les bons paramètres
- [ ] mysqlclient ou pymysql installé
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Superutilisateur créé
- [ ] Fichiers statiques collectés (`python manage.py collectstatic`)
- [ ] Web App configurée
- [ ] Fichier WSGI configuré
- [ ] Static files configurés
- [ ] Application rechargée (bouton Reload)
- [ ] Site accessible et fonctionnel

## 🔄 Mise à jour de l'application

Pour mettre à jour votre application après des modifications :

```bash
cd ~/ETRAGC_SARLU
git pull  # si vous utilisez Git
python manage.py migrate
python manage.py collectstatic --noinput
```

Puis cliquez sur **Reload** dans l'onglet Web.

## 💾 Sauvegarde de la base de données

Pour sauvegarder votre base de données :

```bash
mysqldump -u ETRAGCSARLU -h ETRAGCSARLU.mysql.pythonanywhere-services.com 'ETRAGCSARLU$par défaut' > backup_$(date +%Y%m%d).sql
```

## 📚 Ressources

- Documentation PythonAnywhere : https://help.pythonanywhere.com/
- Django sur PythonAnywhere : https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- MySQL sur PythonAnywhere : https://help.pythonanywhere.com/pages/MySQL/

## 🆘 Support

- Forum PythonAnywhere : https://www.pythonanywhere.com/forums/
- Documentation Django : https://docs.djangoproject.com/

---

**Note:** Avec un compte gratuit PythonAnywhere, vous avez des limitations :
- Connexion MySQL uniquement depuis PythonAnywhere
- Pas d'accès SSH externe
- Domaine en `.pythonanywhere.com`
- Ressources limitées

Pour plus de fonctionnalités, envisagez un compte payant.
