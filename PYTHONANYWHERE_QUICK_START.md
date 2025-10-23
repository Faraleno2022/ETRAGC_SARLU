# 🚀 Démarrage Rapide PythonAnywhere - ETRAGC SARLU

## 📝 Vos informations MySQL

```
Hôte:          ETRAGCSARLU.mysql.pythonanywhere-services.com
Utilisateur:   ETRAGCSARLU
Base de données: ETRAGCSARLU$par défaut
Mot de passe:  [À définir dans PythonAnywhere]
```

## ⚡ Configuration en 5 étapes

### Étape 1: Créer le mot de passe MySQL

1. Connectez-vous à [PythonAnywhere](https://www.pythonanywhere.com)
2. Allez dans l'onglet **Databases**
3. Section **MySQL password**, définissez un nouveau mot de passe
4. **Notez ce mot de passe** (différent de votre mot de passe PythonAnywhere)

### Étape 2: Créer la base de données

Dans l'onglet **Databases** :
- Nom de la base : `par défaut`
- Cliquez sur **Create**
- La base `ETRAGCSARLU$par défaut` sera créée automatiquement

### Étape 3: Configurer le fichier .env

Créez ou modifiez le fichier `.env` sur PythonAnywhere :

```bash
nano ~/.env
```

Ajoutez :

```env
# Configuration ETRAGC SARLU
SECRET_KEY=changez-cette-cle-secrete-par-une-longue-chaine-aleatoire
DEBUG=False
ALLOWED_HOSTS=ETRAGCSARLU.pythonanywhere.com

# Base de données MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=ETRAGCSARLU$par défaut
DB_USER=ETRAGCSARLU
DB_PASSWORD=VOTRE_MOT_DE_PASSE_MYSQL_ICI
DB_HOST=ETRAGCSARLU.mysql.pythonanywhere-services.com
DB_PORT=3306

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

**N'oubliez pas de remplacer `VOTRE_MOT_DE_PASSE_MYSQL_ICI`!**

### Étape 4: Installer les dépendances

Dans une console Bash PythonAnywhere :

```bash
cd ~/ETRAGC_SARLU
pip install --user -r requirements.txt
pip install --user mysqlclient
```

Si `mysqlclient` pose problème, utilisez `pymysql` :

```bash
pip install --user pymysql
```

Et ajoutez dans `config/__init__.py` :

```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Étape 5: Initialiser la base de données

```bash
cd ~/ETRAGC_SARLU
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 🌐 Configuration Web App

### 1. Créer une Web App

Onglet **Web** → **Add a new web app** :
- Domaine : `ETRAGCSARLU.pythonanywhere.com`
- Framework : **Manual configuration**
- Version Python : **3.10** (ou votre version)

### 2. Configurer le fichier WSGI

Cliquez sur le lien du fichier WSGI et remplacez tout par :

```python
import os
import sys

# Chemin vers votre projet
path = '/home/ETRAGCSARLU/ETRAGC_SARLU'
if path not in sys.path:
    sys.path.append(path)

# Charger les variables d'environnement
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/ETRAGC_SARLU')
load_dotenv(os.path.join(project_folder, '.env'))

# Configuration Django
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

### 4. Recharger l'application

Cliquez sur le gros bouton vert **Reload** en haut de la page.

## ✅ Vérification

Visitez : `https://ETRAGCSARLU.pythonanywhere.com`

Vous devriez voir votre application ETRAGC SARLU !

## 🔧 Commandes utiles

### Vérifier la configuration

```bash
python check_mysql_config.py
```

### Tester la connexion MySQL

```bash
python manage.py dbshell
```

### Voir les logs d'erreur

Dans l'onglet **Web**, cliquez sur les liens des logs :
- Error log
- Server log

### Mettre à jour l'application

```bash
cd ~/ETRAGC_SARLU
git pull  # si vous utilisez Git
python manage.py migrate
python manage.py collectstatic --noinput
```

Puis **Reload** dans l'onglet Web.

## ⚠️ Problèmes courants

### "Can't connect to MySQL server"

✓ Vérifiez le hostname : `ETRAGCSARLU.mysql.pythonanywhere-services.com`  
✓ Vérifiez le nom de la base : `ETRAGCSARLU$par défaut` (avec le $)  
✓ Vérifiez le mot de passe dans `.env`

### "No module named 'MySQLdb'"

```bash
pip install --user mysqlclient
# ou
pip install --user pymysql
```

### "DisallowedHost"

Ajoutez dans `.env` :
```env
ALLOWED_HOSTS=ETRAGCSARLU.pythonanywhere.com
```

### Les fichiers statiques ne chargent pas

```bash
python manage.py collectstatic --noinput
```

Et vérifiez la configuration Static files dans l'onglet Web.

## 📚 Documentation complète

Pour plus de détails, consultez :
- `PYTHONANYWHERE_SETUP.md` - Guide complet
- `MYSQL_SETUP.md` - Configuration MySQL générale
- [Documentation PythonAnywhere](https://help.pythonanywhere.com/)

## 🆘 Besoin d'aide ?

1. Vérifiez les logs d'erreur dans l'onglet Web
2. Exécutez `python check_mysql_config.py`
3. Consultez le forum PythonAnywhere
4. Vérifiez la documentation Django

---

**Bon déploiement ! 🚀**
