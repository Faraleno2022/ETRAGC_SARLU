#!/usr/bin/env python
"""
Script de vérification de la configuration MySQL pour ETRAGC SARLU
Vérifie que tous les paramètres MySQL sont correctement configurés
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

def check_mysql_config():
    """Vérifie la configuration MySQL"""
    
    print("=" * 60)
    print("VÉRIFICATION DE LA CONFIGURATION MYSQL")
    print("=" * 60)
    print()
    
    # Récupérer les variables d'environnement
    db_engine = os.getenv('DB_ENGINE', '')
    db_name = os.getenv('DB_NAME', '')
    db_user = os.getenv('DB_USER', '')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', '')
    db_port = os.getenv('DB_PORT', '')
    
    # Vérifier le moteur de base de données
    print("1. Moteur de base de données")
    print(f"   DB_ENGINE: {db_engine}")
    if 'mysql' in db_engine.lower():
        print("   ✓ MySQL configuré")
    else:
        print("   ✗ MySQL n'est pas configuré")
        print("   → Modifiez DB_ENGINE dans .env")
        return False
    print()
    
    # Vérifier les paramètres de connexion
    print("2. Paramètres de connexion")
    errors = []
    
    if not db_name:
        errors.append("DB_NAME n'est pas défini")
    else:
        print(f"   ✓ DB_NAME: {db_name}")
    
    if not db_user:
        errors.append("DB_USER n'est pas défini")
    else:
        print(f"   ✓ DB_USER: {db_user}")
    
    if not db_password:
        errors.append("DB_PASSWORD n'est pas défini")
    else:
        print(f"   ✓ DB_PASSWORD: {'*' * len(db_password)} (masqué)")
    
    if not db_host:
        errors.append("DB_HOST n'est pas défini")
    else:
        print(f"   ✓ DB_HOST: {db_host}")
    
    if not db_port:
        errors.append("DB_PORT n'est pas défini")
    else:
        print(f"   ✓ DB_PORT: {db_port}")
    
    if errors:
        print()
        print("   Erreurs détectées:")
        for error in errors:
            print(f"   ✗ {error}")
        return False
    print()
    
    # Vérifier si c'est PythonAnywhere
    print("3. Type d'hébergement")
    if 'pythonanywhere' in db_host.lower():
        print("   ✓ Configuration PythonAnywhere détectée")
        print(f"   → Assurez-vous d'exécuter ce code sur PythonAnywhere")
        print(f"   → Les comptes gratuits ne peuvent se connecter que depuis PythonAnywhere")
    else:
        print("   ℹ Configuration locale ou serveur personnalisé")
    print()
    
    # Tester la connexion
    print("4. Test de connexion à la base de données")
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"   ✓ Connexion réussie!")
            print(f"   ℹ Version MySQL: {version}")
        
        # Vérifier les tables
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ✓ {len(tables)} table(s) trouvée(s) dans la base de données")
        else:
            print("   ⚠ Aucune table trouvée")
            print("   → Exécutez: python manage.py migrate")
        
        return True
        
    except ImportError as e:
        print(f"   ✗ Erreur d'import: {e}")
        print("   → Installez les dépendances: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"   ✗ Erreur de connexion: {e}")
        print()
        print("   Vérifications à faire:")
        print("   1. Le serveur MySQL est-il démarré?")
        print("   2. Les identifiants sont-ils corrects?")
        print("   3. La base de données existe-t-elle?")
        print("   4. mysqlclient ou pymysql est-il installé?")
        print()
        print("   Commandes utiles:")
        print("   - Installer mysqlclient: pip install mysqlclient")
        print("   - Installer pymysql: pip install pymysql")
        print("   - Vérifier Django: python manage.py check")
        return False

def show_pythonanywhere_info():
    """Affiche les informations spécifiques à PythonAnywhere"""
    print()
    print("=" * 60)
    print("INFORMATIONS PYTHONANYWHERE")
    print("=" * 60)
    print()
    print("Configuration attendue pour PythonAnywhere:")
    print()
    print("DB_ENGINE=django.db.backends.mysql")
    print("DB_NAME=ETRAGCSARLU$par défaut")
    print("DB_USER=ETRAGCSARLU")
    print("DB_PASSWORD=votre_mot_de_passe_mysql")
    print("DB_HOST=ETRAGCSARLU.mysql.pythonanywhere-services.com")
    print("DB_PORT=3306")
    print()
    print("⚠️  IMPORTANT:")
    print("- Le mot de passe MySQL doit être différent du mot de passe PythonAnywhere")
    print("- Avec un compte gratuit, la connexion MySQL ne fonctionne que depuis PythonAnywhere")
    print("- Le nom de la base de données doit commencer par 'ETRAGCSARLU$'")
    print()
    print("📚 Documentation:")
    print("- Voir PYTHONANYWHERE_SETUP.md pour le guide complet")
    print()

def main():
    """Fonction principale"""
    
    # Vérifier si le fichier .env existe
    env_file = BASE_DIR / '.env'
    if not env_file.exists():
        print("=" * 60)
        print("ERREUR: Fichier .env introuvable")
        print("=" * 60)
        print()
        print("Le fichier .env n'existe pas dans le répertoire du projet.")
        print()
        print("Actions à faire:")
        print("1. Copiez .env.example vers .env:")
        print("   cp .env.example .env")
        print()
        print("2. Modifiez .env avec vos paramètres MySQL")
        print()
        return
    
    # Vérifier la configuration
    success = check_mysql_config()
    
    # Afficher les informations PythonAnywhere si applicable
    db_host = os.getenv('DB_HOST', '')
    if 'pythonanywhere' in db_host.lower():
        show_pythonanywhere_info()
    
    # Résumé
    print("=" * 60)
    if success:
        print("✓ CONFIGURATION MYSQL VALIDE")
        print()
        print("Prochaines étapes:")
        print("1. python manage.py migrate")
        print("2. python manage.py createsuperuser")
        print("3. python manage.py runserver")
    else:
        print("✗ CONFIGURATION MYSQL INVALIDE")
        print()
        print("Consultez les messages ci-dessus pour corriger les erreurs.")
    print("=" * 60)

if __name__ == '__main__':
    main()
