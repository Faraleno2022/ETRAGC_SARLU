"""
Script de vérification de la sécurité du projet ETRAGC
Usage: python check_security.py
"""

import os
import sys
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def check_env_file():
    """Vérifie la présence et la configuration du fichier .env"""
    print_header("1. Vérification du fichier .env")
    
    if not os.path.exists('.env'):
        print("❌ Fichier .env manquant!")
        print("   Copiez .env.example vers .env et configurez-le.")
        return False
    
    print("✓ Fichier .env présent")
    
    # Vérifier les variables critiques
    with open('.env', 'r') as f:
        content = f.read()
        
        checks = {
            'SECRET_KEY': 'SECRET_KEY' in content and 'your-secret-key' not in content,
            'DEBUG': 'DEBUG' in content,
            'ALLOWED_HOSTS': 'ALLOWED_HOSTS' in content,
            'DB_ENGINE': 'DB_ENGINE' in content,
        }
        
        for key, status in checks.items():
            if status:
                print(f"✓ {key} configuré")
            else:
                print(f"⚠ {key} manquant ou non configuré")
    
    return True

def check_secret_key():
    """Vérifie que la SECRET_KEY est sécurisée"""
    print_header("2. Vérification de la SECRET_KEY")
    
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('SECRET_KEY'):
                    key = line.split('=')[1].strip()
                    if len(key) < 50:
                        print("⚠ SECRET_KEY trop courte (< 50 caractères)")
                    elif 'your-secret-key' in key or 'change' in key.lower():
                        print("❌ SECRET_KEY par défaut détectée!")
                        print("   Générez une nouvelle clé avec:")
                        print("   python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\"")
                    else:
                        print("✓ SECRET_KEY semble sécurisée")
                    return
    except:
        print("❌ Impossible de vérifier la SECRET_KEY")

def check_debug_mode():
    """Vérifie que DEBUG est False en production"""
    print_header("3. Vérification du mode DEBUG")
    
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('DEBUG'):
                    debug = line.split('=')[1].strip().lower()
                    if debug == 'true':
                        print("⚠ DEBUG=True détecté")
                        print("   En production, utilisez DEBUG=False")
                    else:
                        print("✓ DEBUG=False (recommandé pour production)")
                    return
    except:
        print("❌ Impossible de vérifier DEBUG")

def check_dependencies():
    """Vérifie que les packages de sécurité sont installés"""
    print_header("4. Vérification des packages de sécurité")
    
    required_packages = [
        'django-axes',
        'django-ratelimit',
        'django-csp',
        'django-cors-headers',
    ]
    
    try:
        import subprocess
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        installed = result.stdout.lower()
        
        for package in required_packages:
            if package.lower() in installed:
                print(f"✓ {package} installé")
            else:
                print(f"❌ {package} manquant")
                print(f"   Installez avec: pip install {package}")
    except:
        print("⚠ Impossible de vérifier les packages")
        print("  Exécutez: pip install -r requirements.txt")

def check_logs_directory():
    """Vérifie que le dossier logs existe"""
    print_header("5. Vérification du dossier logs")
    
    if os.path.exists('logs'):
        print("✓ Dossier logs présent")
        
        # Vérifier les permissions
        if os.access('logs', os.W_OK):
            print("✓ Dossier logs accessible en écriture")
        else:
            print("❌ Dossier logs non accessible en écriture")
    else:
        print("❌ Dossier logs manquant")
        print("   Créez-le avec: mkdir logs")

def check_database_security():
    """Vérifie la configuration de la base de données"""
    print_header("6. Vérification de la base de données")
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            
            if 'DB_ENGINE=django.db.backends.sqlite3' in content:
                print("⚠ SQLite détecté (OK pour développement)")
                print("  Pour production, utilisez MySQL ou PostgreSQL")
            elif 'DB_ENGINE=django.db.backends.mysql' in content:
                print("✓ MySQL configuré")
                
                # Vérifier le mot de passe
                for line in content.split('\n'):
                    if line.startswith('DB_PASSWORD'):
                        pwd = line.split('=')[1].strip()
                        if not pwd or pwd == '':
                            print("❌ Mot de passe de base de données vide!")
                        else:
                            print("✓ Mot de passe de base de données configuré")
            elif 'DB_ENGINE=django.db.backends.postgresql' in content:
                print("✓ PostgreSQL configuré")
    except:
        print("❌ Impossible de vérifier la configuration de la base de données")

def check_allowed_hosts():
    """Vérifie ALLOWED_HOSTS"""
    print_header("7. Vérification de ALLOWED_HOSTS")
    
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ALLOWED_HOSTS'):
                    hosts = line.split('=')[1].strip()
                    if 'localhost' in hosts and '127.0.0.1' in hosts:
                        print("⚠ ALLOWED_HOSTS contient localhost/127.0.0.1")
                        print("  En production, spécifiez votre domaine")
                    else:
                        print("✓ ALLOWED_HOSTS configuré")
                    return
    except:
        print("❌ Impossible de vérifier ALLOWED_HOSTS")

def check_gitignore():
    """Vérifie que .env est dans .gitignore"""
    print_header("8. Vérification de .gitignore")
    
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            content = f.read()
            if '.env' in content:
                print("✓ .env est dans .gitignore")
            else:
                print("❌ .env n'est PAS dans .gitignore!")
                print("   Ajoutez-le immédiatement!")
            
            if 'logs/*.log' in content or '*.log' in content:
                print("✓ Fichiers logs ignorés")
            else:
                print("⚠ Fichiers logs non ignorés")
    else:
        print("❌ Fichier .gitignore manquant!")

def run_django_check():
    """Exécute le check de sécurité Django"""
    print_header("9. Django Security Check")
    
    try:
        import subprocess
        result = subprocess.run(
            ['python', 'manage.py', 'check', '--deploy'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Aucun problème détecté par Django")
        else:
            print("⚠ Django a détecté des problèmes:")
            print(result.stdout)
    except:
        print("⚠ Impossible d'exécuter 'python manage.py check --deploy'")

def print_summary():
    """Affiche un résumé et des recommandations"""
    print_header("RÉSUMÉ ET RECOMMANDATIONS")
    
    print("""
    📋 Checklist de Sécurité:
    
    [ ] SECRET_KEY unique et sécurisée (50+ caractères)
    [ ] DEBUG=False en production
    [ ] ALLOWED_HOSTS configuré avec votre domaine
    [ ] Base de données avec mot de passe fort
    [ ] Packages de sécurité installés
    [ ] HTTPS activé (certificat SSL)
    [ ] Sauvegardes régulières configurées
    [ ] Logs surveillés
    [ ] .env dans .gitignore
    [ ] Firewall configuré
    
    🔒 Prochaines étapes:
    
    1. Installer les packages:
       pip install -r requirements.txt
    
    2. Appliquer les migrations:
       python manage.py migrate
    
    3. Tester l'application:
       python manage.py runserver
    
    4. En production:
       - Activer HTTPS
       - Configurer le firewall
       - Mettre en place les sauvegardes
       - Surveiller les logs
    
    📚 Documentation:
       Consultez SECURITY.md pour plus de détails
    """)

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     VÉRIFICATION DE SÉCURITÉ - ETRAGC SARLU               ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Vérifier qu'on est dans le bon dossier
    if not os.path.exists('manage.py'):
        print("❌ Erreur: Ce script doit être exécuté depuis la racine du projet")
        print("   (le dossier contenant manage.py)")
        return
    
    # Exécuter toutes les vérifications
    check_env_file()
    check_secret_key()
    check_debug_mode()
    check_dependencies()
    check_logs_directory()
    check_database_security()
    check_allowed_hosts()
    check_gitignore()
    run_django_check()
    print_summary()
    
    print("\n✅ Vérification terminée!\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Vérification interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
