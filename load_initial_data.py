"""
Script pour charger les données initiales dans la base de données ETRAGC
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.finances.models import CategorieDepense
from apps.core.models import Parametre

print("🚀 Chargement des données initiales...")

# Catégories de dépenses
print("\n📦 Création des catégories de dépenses...")
categories = [
    {
        'nom': 'Matériaux de Construction',
        'code': 'MAT',
        'couleur_hex': '#3B82F6',
        'description': 'Ciment, sable, gravier, fer, bois, etc.',
        'ordre': 1
    },
    {
        'nom': 'Main d\'Œuvre',
        'code': 'MO',
        'couleur_hex': '#10B981',
        'description': 'Salaires ouvriers, artisans, techniciens',
        'ordre': 2
    },
    {
        'nom': 'Location Équipement',
        'code': 'LOC',
        'couleur_hex': '#F59E0B',
        'description': 'Engins, échafaudages, outils',
        'ordre': 3
    },
    {
        'nom': 'Carburant et Transport',
        'code': 'TRANS',
        'couleur_hex': '#EF4444',
        'description': 'Essence, gasoil, transport matériaux',
        'ordre': 4
    },
    {
        'nom': 'Électricité et Eau',
        'code': 'ELEC',
        'couleur_hex': '#8B5CF6',
        'description': 'Consommations chantier',
        'ordre': 5
    },
    {
        'nom': 'Restauration',
        'code': 'REST',
        'couleur_hex': '#EC4899',
        'description': 'Repas équipes',
        'ordre': 6
    },
    {
        'nom': 'Fournitures Diverses',
        'code': 'FOUR',
        'couleur_hex': '#6366F1',
        'description': 'Petits matériels, consommables',
        'ordre': 7
    },
    {
        'nom': 'Sous-traitance',
        'code': 'ST',
        'couleur_hex': '#14B8A6',
        'description': 'Prestataires externes',
        'ordre': 8
    },
    {
        'nom': 'Assurances et Taxes',
        'code': 'TAX',
        'couleur_hex': '#F97316',
        'description': 'Cotisations, taxes chantier',
        'ordre': 9
    },
    {
        'nom': 'Autres',
        'code': 'AUT',
        'couleur_hex': '#64748B',
        'description': 'Dépenses non catégorisées',
        'ordre': 10
    },
]

for cat in categories:
    obj, created = CategorieDepense.objects.get_or_create(
        code=cat['code'],
        defaults={
            'nom': cat['nom'],
            'couleur_hex': cat['couleur_hex'],
            'description': cat['description'],
            'ordre_affichage': cat['ordre']
        }
    )
    if created:
        print(f"  ✅ {cat['nom']} créée")
    else:
        print(f"  ℹ️  {cat['nom']} existe déjà")

# Paramètres de l'entreprise
print("\n⚙️  Configuration des paramètres de l'entreprise...")
parametres = [
    {
        'cle': 'entreprise_nom',
        'valeur': 'ÉLITE DES TRAVAUX DE GÉNIE CIVIL SARLU',
        'description': 'Nom de l\'entreprise',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_sigle',
        'valeur': 'ETRAGC SARLU',
        'description': 'Sigle de l\'entreprise',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_rccm',
        'valeur': 'GN.TCC.2024.B.02513',
        'description': 'Numéro RCCM',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_nif',
        'valeur': '797139748',
        'description': 'Numéro NIF',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_tva',
        'valeur': '2X',
        'description': 'Numéro TVA',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_email',
        'valeur': 'info@etragc-sarlu.com',
        'description': 'Email principal',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_telephone',
        'valeur': '+224 628 78 78 03',
        'description': 'Téléphone principal',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_telephone_2',
        'valeur': '+224 612 79 79 03',
        'description': 'Téléphone secondaire',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_adresse',
        'valeur': 'Kankan, Quartier Missira',
        'description': 'Adresse du siège',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'entreprise_site_web',
        'valeur': 'www.etragc-sarlu.com',
        'description': 'Site web',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'taux_tva_defaut',
        'valeur': '18.00',
        'description': 'Taux TVA par défaut (%)',
        'type_donnee': 'Nombre'
    },
    {
        'cle': 'devise',
        'valeur': 'GNF',
        'description': 'Devise utilisée',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'prefix_projet',
        'valeur': 'PROJ',
        'description': 'Préfixe code projet',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'prefix_devis',
        'valeur': 'DEV',
        'description': 'Préfixe numéro devis',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'prefix_facture',
        'valeur': 'FACT',
        'description': 'Préfixe numéro facture',
        'type_donnee': 'Texte'
    },
    {
        'cle': 'delai_paiement_defaut',
        'valeur': '30',
        'description': 'Délai paiement par défaut (jours)',
        'type_donnee': 'Nombre'
    },
]

for param in parametres:
    obj, created = Parametre.objects.get_or_create(
        cle=param['cle'],
        defaults={
            'valeur': param['valeur'],
            'description': param['description'],
            'type_donnee': param['type_donnee']
        }
    )
    if created:
        print(f"  ✅ {param['cle']} créé")
    else:
        print(f"  ℹ️  {param['cle']} existe déjà")

print("\n✨ Données initiales chargées avec succès!")
print("\n📝 Prochaines étapes:")
print("  1. Créer un superutilisateur : python manage.py createsuperuser")
print("  2. Lancer le serveur : python manage.py runserver")
print("  3. Accéder à l'admin : http://127.0.0.1:8000/admin")
