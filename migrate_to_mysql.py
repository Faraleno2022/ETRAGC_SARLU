"""
Script d'aide pour migrer de SQLite vers MySQL
Usage: python migrate_to_mysql.py
"""

import os
import sys
import subprocess

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"ÉTAPE {step}: {message}")
    print('='*60)

def run_command(command, description):
    print(f"\n▶ {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ {description} - Succès")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print(f"✗ {description} - Erreur")
        if result.stderr:
            print(result.stderr)
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     MIGRATION SQLite → MySQL pour ETRAGC SARLU            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Vérifications préliminaires
    print_step(1, "Vérifications préliminaires")
    
    if not os.path.exists('.env'):
        print("⚠ Fichier .env non trouvé!")
        print("Copiez .env.example vers .env et configurez-le d'abord.")
        return
    
    # Sauvegarde SQLite
    print_step(2, "Sauvegarde des données SQLite")
    
    backup_file = 'data_backup.json'
    if os.path.exists(backup_file):
        response = input(f"Le fichier {backup_file} existe déjà. Écraser? (o/n): ")
        if response.lower() != 'o':
            print("Opération annulée.")
            return
    
    if not run_command(
        f'python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > {backup_file}',
        "Export des données SQLite"
    ):
        print("\n❌ Échec de l'export des données!")
        return
    
    print(f"\n✓ Données sauvegardées dans {backup_file}")
    
    # Configuration MySQL
    print_step(3, "Configuration MySQL")
    print("""
    Assurez-vous d'avoir:
    1. ✓ MySQL Server installé et démarré
    2. ✓ Base de données créée (etragc_db)
    3. ✓ Fichier .env configuré avec les paramètres MySQL
    
    Exemple de configuration .env:
    DB_ENGINE=django.db.backends.mysql
    DB_NAME=etragc_db
    DB_USER=root
    DB_PASSWORD=votre_mot_de_passe
    DB_HOST=localhost
    DB_PORT=3306
    """)
    
    response = input("\nConfiguration MySQL terminée? (o/n): ")
    if response.lower() != 'o':
        print("\nConfigurez MySQL et relancez ce script.")
        return
    
    # Test de connexion
    print_step(4, "Test de connexion MySQL")
    
    if not run_command('python manage.py check', "Vérification de la configuration"):
        print("\n❌ Erreur de configuration! Vérifiez votre fichier .env")
        return
    
    # Migrations
    print_step(5, "Application des migrations")
    
    if not run_command('python manage.py migrate', "Création des tables MySQL"):
        print("\n❌ Échec des migrations!")
        return
    
    # Import des données
    print_step(6, "Import des données")
    
    response = input("\nImporter les données depuis SQLite? (o/n): ")
    if response.lower() == 'o':
        if not run_command(f'python manage.py loaddata {backup_file}', "Import des données"):
            print("\n⚠ Erreur lors de l'import des données!")
            print("Vous pouvez réessayer manuellement avec:")
            print(f"python manage.py loaddata {backup_file}")
        else:
            print("\n✓ Données importées avec succès!")
    
    # Création du superutilisateur
    print_step(7, "Superutilisateur")
    
    response = input("\nCréer un nouveau superutilisateur? (o/n): ")
    if response.lower() == 'o':
        run_command('python manage.py createsuperuser', "Création du superutilisateur")
    
    # Finalisation
    print_step(8, "Finalisation")
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              MIGRATION TERMINÉE AVEC SUCCÈS!              ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Prochaines étapes:
    
    1. Tester l'application:
       python manage.py runserver
    
    2. Vérifier que toutes les données sont présentes
    
    3. Faire une sauvegarde MySQL:
       mysqldump -u root -p etragc_db > backup.sql
    
    4. Supprimer l'ancien fichier SQLite (optionnel):
       del db.sqlite3
    
    5. Garder le fichier de sauvegarde:
       {backup_file}
    
    ✓ Votre application utilise maintenant MySQL!
    """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Opération annulée par l'utilisateur.")
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue: {e}")
