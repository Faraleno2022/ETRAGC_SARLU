# Configuration MySQL pour ETRAGC SARLU

## 📋 Prérequis

1. **MySQL Server** installé (version 5.7 ou supérieure recommandée)
2. **Python 3.8+** installé
3. **Visual Studio Build Tools** (pour Windows) ou **build-essential** (pour Linux)

## 🔧 Installation de MySQL sur Windows

### Option 1: MySQL Installer
1. Télécharger MySQL Installer depuis https://dev.mysql.com/downloads/installer/
2. Installer MySQL Server
3. Configurer le mot de passe root
4. Démarrer le service MySQL

### Option 2: Via Chocolatey
```powershell
choco install mysql
```

## 📦 Installation des dépendances Python

### 1. Installer mysqlclient

**Sur Windows:**
```powershell
pip install mysqlclient
```

Si vous rencontrez des erreurs, installez d'abord:
- Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
- Ou utilisez une wheel précompilée: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

**Alternative avec PyMySQL (plus simple sur Windows):**
```powershell
pip install pymysql
```

Puis ajoutez dans `config/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 🗄️ Création de la base de données MySQL

### 1. Se connecter à MySQL
```bash
mysql -u root -p
```

### 2. Créer la base de données
```sql
CREATE DATABASE etragc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Créer un utilisateur (optionnel mais recommandé)
```sql
CREATE USER 'etragc_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON etragc_db.* TO 'etragc_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## ⚙️ Configuration du projet

### 1. Modifier le fichier `.env`

Remplacez les lignes de configuration de la base de données par:

```env
# Base de données MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=etragc_db
DB_USER=etragc_user
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

**Ou si vous utilisez root:**
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=etragc_db
DB_USER=root
DB_PASSWORD=votre_mot_de_passe_root
DB_HOST=localhost
DB_PORT=3306
```

### 2. Vérifier la configuration
```powershell
python manage.py check
```

## 🔄 Migration des données

### 1. Appliquer les migrations
```powershell
python manage.py migrate
```

### 2. Créer un superutilisateur
```powershell
python manage.py createsuperuser
```

### 3. Charger les données initiales (optionnel)
```powershell
python load_initial_data.py
```

## 📊 Migration depuis SQLite vers MySQL

Si vous avez déjà des données dans SQLite et voulez les migrer vers MySQL:

### 1. Exporter les données depuis SQLite
```powershell
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > data_backup.json
```

### 2. Configurer MySQL dans `.env`

### 3. Créer les tables dans MySQL
```powershell
python manage.py migrate
```

### 4. Importer les données
```powershell
python manage.py loaddata data_backup.json
```

## 🧪 Test de la connexion

```powershell
python manage.py dbshell
```

Cela devrait ouvrir le shell MySQL si la connexion fonctionne.

## 🚀 Démarrer le serveur

```powershell
python manage.py runserver
```

## ⚠️ Problèmes courants

### Erreur: "No module named 'MySQLdb'"
**Solution:** Installer mysqlclient ou pymysql

### Erreur: "Can't connect to MySQL server"
**Solution:** 
- Vérifier que MySQL est démarré: `net start MySQL80` (Windows)
- Vérifier HOST et PORT dans `.env`
- Vérifier le pare-feu

### Erreur: "Access denied for user"
**Solution:** Vérifier USER et PASSWORD dans `.env`

### Erreur de compilation mysqlclient sur Windows
**Solution:** 
- Installer Visual Studio Build Tools
- Ou utiliser PyMySQL comme alternative

## 📝 Configuration de production

Pour la production, ajoutez ces paramètres dans `.env`:

```env
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
DB_HOST=votre-serveur-mysql.com
DB_PORT=3306
```

## 🔐 Sécurité

1. **Ne jamais commiter le fichier `.env`** (déjà dans .gitignore)
2. Utiliser des mots de passe forts
3. Limiter les privilèges de l'utilisateur MySQL
4. Activer SSL pour les connexions distantes
5. Faire des sauvegardes régulières:

```bash
mysqldump -u etragc_user -p etragc_db > backup_$(date +%Y%m%d).sql
```

## 📚 Ressources

- Documentation Django MySQL: https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes
- Documentation MySQL: https://dev.mysql.com/doc/
- mysqlclient: https://github.com/PyMySQL/mysqlclient

## ✅ Checklist de migration

- [ ] MySQL Server installé et démarré
- [ ] Base de données créée
- [ ] Utilisateur MySQL créé (optionnel)
- [ ] mysqlclient ou pymysql installé
- [ ] Fichier `.env` configuré
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Données migrées (si nécessaire)
- [ ] Test de connexion réussi
- [ ] Application fonctionne correctement
