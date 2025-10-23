# 📦 Guide d'Installation - ETRAGC SARLU

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.10 ou supérieur** : [Télécharger Python](https://www.python.org/downloads/)
- **MySQL 8.0 ou supérieur** : [Télécharger MySQL](https://dev.mysql.com/downloads/)
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel) : [Télécharger Git](https://git-scm.com/downloads/)

## Étape 1 : Préparation de l'environnement

### 1.1 Vérifier Python
```bash
python --version
# Doit afficher Python 3.10 ou supérieur
```

### 1.2 Vérifier pip
```bash
pip --version
```

## Étape 2 : Configuration de la base de données MySQL

### 2.1 Démarrer MySQL
Lancez MySQL depuis votre panneau de configuration ou en ligne de commande.

### 2.2 Créer la base de données
Connectez-vous à MySQL et exécutez :

```sql
CREATE DATABASE etragc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2.3 Créer un utilisateur (optionnel mais recommandé)
```sql
CREATE USER 'etragc_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe_securise';
GRANT ALL PRIVILEGES ON etragc_db.* TO 'etragc_user'@'localhost';
FLUSH PRIVILEGES;
```

## Étape 3 : Installation du projet

### 3.1 Naviguer vers le répertoire du projet
```bash
cd C:\Users\LENO\Desktop\Etragsarlu
```

### 3.2 Créer un environnement virtuel
```bash
python -m venv venv
```

### 3.3 Activer l'environnement virtuel

**Sur Windows :**
```bash
venv\Scripts\activate
```

**Sur Linux/Mac :**
```bash
source venv/bin/activate
```

Vous devriez voir `(venv)` apparaître au début de votre ligne de commande.

### 3.4 Installer les dépendances
```bash
pip install -r requirements.txt
```

Cette commande installera :
- Django 4.2.7
- mysqlclient (pilote MySQL)
- Pillow (traitement d'images)
- ReportLab (génération PDF)
- Et toutes les autres dépendances

## Étape 4 : Configuration de l'application

### 4.1 Vérifier le fichier .env
Le fichier `.env` contient déjà les paramètres par défaut. Modifiez-le si nécessaire :

```env
DB_NAME=etragc_db
DB_USER=root
DB_PASSWORD=votre_mot_de_passe_mysql
DB_HOST=localhost
DB_PORT=3306
```

### 4.2 Tester la connexion à la base de données
```bash
python manage.py check
```

Si tout est OK, vous devriez voir : `System check identified no issues (0 silenced).`

## Étape 5 : Création de la structure de la base de données

### 5.1 Créer les migrations
```bash
python manage.py makemigrations
```

### 5.2 Appliquer les migrations
```bash
python manage.py migrate
```

Cette commande créera toutes les tables nécessaires dans votre base de données.

## Étape 6 : Création du superutilisateur

### 6.1 Créer un compte administrateur
```bash
python manage.py createsuperuser
```

Suivez les instructions :
- **Nom d'utilisateur** : admin (ou votre choix)
- **Email** : admin@etragc-sarlu.com
- **Mot de passe** : Choisissez un mot de passe sécurisé

## Étape 7 : Charger les données initiales (optionnel)

### 7.1 Créer les catégories de dépenses par défaut
Créez un fichier `load_initial_data.py` dans le répertoire racine :

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.finances.models import CategorieDepense

categories = [
    {'nom': 'Matériaux de Construction', 'code': 'MAT', 'couleur_hex': '#3B82F6', 'ordre': 1},
    {'nom': 'Main d\'Œuvre', 'code': 'MO', 'couleur_hex': '#10B981', 'ordre': 2},
    {'nom': 'Location Équipement', 'code': 'LOC', 'couleur_hex': '#F59E0B', 'ordre': 3},
    {'nom': 'Carburant et Transport', 'code': 'TRANS', 'couleur_hex': '#EF4444', 'ordre': 4},
    {'nom': 'Électricité et Eau', 'code': 'ELEC', 'couleur_hex': '#8B5CF6', 'ordre': 5},
    {'nom': 'Restauration', 'code': 'REST', 'couleur_hex': '#EC4899', 'ordre': 6},
    {'nom': 'Fournitures Diverses', 'code': 'FOUR', 'couleur_hex': '#6366F1', 'ordre': 7},
    {'nom': 'Sous-traitance', 'code': 'ST', 'couleur_hex': '#14B8A6', 'ordre': 8},
    {'nom': 'Assurances et Taxes', 'code': 'TAX', 'couleur_hex': '#F97316', 'ordre': 9},
    {'nom': 'Autres', 'code': 'AUT', 'couleur_hex': '#64748B', 'ordre': 10},
]

for cat in categories:
    CategorieDepense.objects.get_or_create(
        code=cat['code'],
        defaults={
            'nom': cat['nom'],
            'couleur_hex': cat['couleur_hex'],
            'ordre_affichage': cat['ordre']
        }
    )

print("✅ Catégories de dépenses créées avec succès!")
```

Puis exécutez :
```bash
python load_initial_data.py
```

## Étape 8 : Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

## Étape 9 : Lancer le serveur de développement

```bash
python manage.py runserver
```

Le serveur démarre sur : **http://127.0.0.1:8000/**

## Étape 10 : Accéder à l'application

### 10.1 Interface d'administration
Ouvrez votre navigateur et allez sur :
```
http://127.0.0.1:8000/admin
```

Connectez-vous avec le superutilisateur créé à l'étape 6.

### 10.2 Application principale
```
http://127.0.0.1:8000/
```

## 🎉 Félicitations !

Votre application ETRAGC SARLU est maintenant installée et fonctionnelle !

## 🔧 Dépannage

### Erreur : "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

Si l'installation échoue sur Windows, téléchargez le wheel depuis :
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Erreur : "Access denied for user"
Vérifiez vos identifiants MySQL dans le fichier `.env`

### Erreur : "Can't connect to MySQL server"
Assurez-vous que MySQL est démarré et accessible sur le port 3306

### Erreur de migration
```bash
python manage.py migrate --run-syncdb
```

## 📚 Prochaines étapes

1. Créer des utilisateurs avec différents rôles
2. Ajouter des clients
3. Créer des projets
4. Commencer à utiliser l'application !

## 📞 Support

Pour toute question ou problème :
- Email : info@etragc-sarlu.com
- Téléphone : +224 628 78 78 03

---

**ETRAGC SARLU** - Application de Gestion BTP
Version 1.0 - Octobre 2025
