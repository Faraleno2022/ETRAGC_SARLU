"""
Fichier WSGI pour PythonAnywhere - ETRAGC SARLU

Ce fichier doit être copié dans le fichier WSGI de votre Web App sur PythonAnywhere.
Le chemin du fichier WSGI est généralement:
/var/www/ETRAGCSARLU_pythonanywhere_com_wsgi.py

Instructions:
1. Allez dans l'onglet "Web" de PythonAnywhere
2. Cliquez sur le lien du fichier WSGI
3. Remplacez tout le contenu par ce fichier
4. Modifiez les chemins si nécessaire
5. Cliquez sur "Save" et "Reload"
"""

import os
import sys

# ============================================================================
# CONFIGURATION DES CHEMINS
# ============================================================================

# Chemin vers votre projet Django
# Modifiez 'ETRAGC_SARLU' si votre dossier a un nom différent
project_home = '/home/ETRAGCSARLU/ETRAGC_SARLU'

# Ajouter le répertoire du projet au path Python
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================================================
# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ============================================================================

# Charger les variables d'environnement depuis le fichier .env
from dotenv import load_dotenv

# Chemin vers le fichier .env
env_path = os.path.join(project_home, '.env')

# Charger les variables
load_dotenv(env_path)

# Vérifier que les variables critiques sont chargées
if not os.getenv('SECRET_KEY'):
    print("ATTENTION: SECRET_KEY n'est pas défini dans .env")
if not os.getenv('DB_PASSWORD'):
    print("ATTENTION: DB_PASSWORD n'est pas défini dans .env")

# ============================================================================
# CONFIGURATION DJANGO
# ============================================================================

# Définir le module de configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Importer l'application WSGI Django
from django.core.wsgi import get_wsgi_application

# Créer l'application WSGI
application = get_wsgi_application()

# ============================================================================
# INFORMATIONS DE DÉBOGAGE (à retirer en production)
# ============================================================================

# Afficher les informations de configuration (utile pour le débogage)
print("=" * 60)
print("CONFIGURATION WSGI - ETRAGC SARLU")
print("=" * 60)
print(f"Project home: {project_home}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}...")
print(f"Django settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"DB Engine: {os.getenv('DB_ENGINE', 'Non défini')}")
print(f"DB Host: {os.getenv('DB_HOST', 'Non défini')}")
print(f"DB Name: {os.getenv('DB_NAME', 'Non défini')}")
print(f"Debug mode: {os.getenv('DEBUG', 'Non défini')}")
print("=" * 60)
