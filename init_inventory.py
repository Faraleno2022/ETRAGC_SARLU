#!/usr/bin/env python
"""
Script d'initialisation du module Inventory
Charge les données initiales (unités de mesure et catégories)
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.inventory.models import UniteMessure, CategorieProduit


def init_unites_mesure():
    """Initialise les unités de mesure de base"""
    unites = [
        {'nom': 'Kilogramme', 'symbole': 'kg', 'description': 'Unité de masse'},
        {'nom': 'Mètre', 'symbole': 'm', 'description': 'Unité de longueur'},
        {'nom': 'Mètre carré', 'symbole': 'm²', 'description': 'Unité de surface'},
        {'nom': 'Mètre cube', 'symbole': 'm³', 'description': 'Unité de volume'},
        {'nom': 'Pièce', 'symbole': 'pce', 'description': 'Unité de comptage'},
        {'nom': 'Litre', 'symbole': 'L', 'description': 'Unité de volume liquide'},
        {'nom': 'Sac', 'symbole': 'sac', 'description': 'Unité de conditionnement'},
        {'nom': 'Tonne', 'symbole': 't', 'description': 'Unité de masse (1000 kg)'},
        {'nom': 'Boîte', 'symbole': 'bte', 'description': 'Unité de conditionnement'},
        {'nom': 'Rouleau', 'symbole': 'roul', 'description': 'Unité de conditionnement'},
    ]
    
    created_count = 0
    for unite_data in unites:
        unite, created = UniteMessure.objects.get_or_create(
            symbole=unite_data['symbole'],
            defaults=unite_data
        )
        if created:
            created_count += 1
            print(f"✓ Unité créée: {unite.nom} ({unite.symbole})")
        else:
            print(f"- Unité existante: {unite.nom} ({unite.symbole})")
    
    print(f"\n{created_count} unité(s) de mesure créée(s)")
    return created_count


def init_categories():
    """Initialise les catégories de produits"""
    categories = [
        {'nom': 'Ciment et Liants', 'code': 'CIM', 'description': 'Ciment, chaux, mortier', 'ordre_affichage': 1},
        {'nom': 'Agrégats', 'code': 'AGR', 'description': 'Sable, gravier, pierre', 'ordre_affichage': 2},
        {'nom': 'Fer et Acier', 'code': 'FER', 'description': 'Fers à béton, treillis, profilés', 'ordre_affichage': 3},
        {'nom': 'Bois', 'code': 'BOI', 'description': 'Planches, chevrons, contreplaqué', 'ordre_affichage': 4},
        {'nom': 'Peinture et Finitions', 'code': 'PEI', 'description': 'Peintures, vernis, enduits', 'ordre_affichage': 5},
        {'nom': 'Plomberie', 'code': 'PLO', 'description': 'Tuyaux, raccords, robinetterie', 'ordre_affichage': 6},
        {'nom': 'Électricité', 'code': 'ELE', 'description': 'Câbles, interrupteurs, prises', 'ordre_affichage': 7},
        {'nom': 'Carrelage et Revêtements', 'code': 'CAR', 'description': 'Carreaux, faïence, revêtements', 'ordre_affichage': 8},
        {'nom': 'Quincaillerie', 'code': 'QUI', 'description': 'Clous, vis, serrures, charnières', 'ordre_affichage': 9},
        {'nom': 'Outillage', 'code': 'OUT', 'description': 'Outils de construction', 'ordre_affichage': 10},
        {'nom': 'Matériaux de Couverture', 'code': 'COU', 'description': 'Tuiles, tôles, gouttières', 'ordre_affichage': 11},
        {'nom': 'Menuiserie', 'code': 'MEN', 'description': 'Portes, fenêtres, cadres', 'ordre_affichage': 12},
    ]
    
    created_count = 0
    for cat_data in categories:
        categorie, created = CategorieProduit.objects.get_or_create(
            code=cat_data['code'],
            defaults=cat_data
        )
        if created:
            created_count += 1
            print(f"✓ Catégorie créée: {categorie.nom} ({categorie.code})")
        else:
            print(f"- Catégorie existante: {categorie.nom} ({categorie.code})")
    
    print(f"\n{created_count} catégorie(s) créée(s)")
    return created_count


def main():
    """Fonction principale"""
    print("=" * 60)
    print("INITIALISATION DU MODULE INVENTORY")
    print("=" * 60)
    print()
    
    print("1. Initialisation des unités de mesure...")
    print("-" * 60)
    unites_count = init_unites_mesure()
    
    print()
    print("2. Initialisation des catégories de produits...")
    print("-" * 60)
    categories_count = init_categories()
    
    print()
    print("=" * 60)
    print("INITIALISATION TERMINÉE")
    print("=" * 60)
    print(f"Total: {unites_count} unités et {categories_count} catégories créées")
    print()
    print("Vous pouvez maintenant:")
    print("1. Créer des produits via l'interface web")
    print("2. Créer des achats et gérer les stocks")
    print("3. Accéder au module via: http://localhost:8000/inventory/")
    print()


if __name__ == '__main__':
    main()
