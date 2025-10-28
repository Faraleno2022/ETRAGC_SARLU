# Module de Gestion de Stock (Inventory)

## Description

Ce module permet de gérer l'inventaire et les achats de produits pour les projets de construction. Il offre un suivi complet des stocks, des mouvements, et des achats avec des alertes automatiques pour les stocks faibles.

## Fonctionnalités

### 1. Gestion des Produits
- Création et gestion des produits/matériaux
- Catégorisation des produits
- Unités de mesure personnalisables
- Prix unitaire moyen calculé automatiquement
- Seuil de stock minimum configurable

### 2. Gestion des Stocks
- Stock par projet
- Suivi de la quantité actuelle
- Valeur du stock calculée automatiquement
- Emplacement physique
- Alertes automatiques pour stocks faibles

### 3. Gestion des Achats
- Création de bons d'achat
- Workflow de validation (Brouillon → Validé → Reçu)
- Lignes d'achat détaillées
- Mise à jour automatique des stocks à la réception
- Pièces justificatives
- Suivi des fournisseurs

### 4. Mouvements de Stock
- Entrées (réception, retour)
- Sorties (utilisation, vente)
- Ajustements (inventaire, correction)
- Transferts entre projets
- Historique complet des mouvements

### 5. Alertes et Rapports
- Alertes de stock faible par projet
- Dashboard avec statistiques
- Historique des mouvements
- Valeur totale du stock
- Top projets par valeur de stock

## Modèles de Données

### UniteMessure
- Unités de mesure (kg, m, m², pièce, etc.)

### CategorieProduit
- Catégories de produits (Ciment, Fer, Bois, etc.)

### Produit
- Code produit (auto-généré)
- Nom, description
- Catégorie et unité de mesure
- Prix unitaire moyen
- Stock minimum

### Stock
- Lien Projet-Produit
- Quantité actuelle
- Valeur du stock
- Emplacement
- Dates de dernière entrée/sortie

### Achat
- Numéro d'achat (auto-généré)
- Projet et fournisseur
- Date d'achat et de réception
- Montant total (calculé)
- Statut (Brouillon, Validé, Reçu, Annulé)
- Mode de paiement

### LigneAchat
- Produit, quantité, prix unitaire
- Montant ligne (calculé)

### MouvementStock
- Type (Entrée, Sortie, Ajustement, Transfert)
- Quantité
- Quantités avant/après
- Motif
- Utilisateur

## Installation

### 1. Créer les migrations
```bash
python manage.py makemigrations inventory
```

### 2. Appliquer les migrations
```bash
python manage.py migrate inventory
```

### 3. Charger les données initiales
```bash
python manage.py loaddata apps/inventory/fixtures/initial_data.json
```

Cela créera :
- 8 unités de mesure de base
- 10 catégories de produits

## Utilisation

### Accès au module
Le module est accessible via le menu principal : **Stock**

### Workflow typique

1. **Configuration initiale**
   - Créer les produits nécessaires
   - Définir les stocks minimum

2. **Création d'un achat**
   - Créer un bon d'achat (statut: Brouillon)
   - Ajouter les lignes d'achat (produits)
   - Valider l'achat
   - Marquer comme reçu → Les stocks sont automatiquement mis à jour

3. **Gestion des stocks**
   - Consulter les stocks par projet
   - Effectuer des mouvements (entrées/sorties)
   - Transférer entre projets
   - Surveiller les alertes

4. **Suivi**
   - Dashboard pour vue d'ensemble
   - Alertes de stock faible
   - Historique des mouvements
   - Rapports par projet

## URLs

- `/inventory/` - Dashboard
- `/inventory/produits/` - Liste des produits
- `/inventory/stocks/` - Liste des stocks
- `/inventory/achats/` - Liste des achats
- `/inventory/mouvements/` - Liste des mouvements
- `/inventory/alertes/` - Alertes de stock

## Permissions

Le module utilise le système d'authentification Django standard. Tous les utilisateurs authentifiés peuvent accéder au module.

Pour des permissions plus granulaires, vous pouvez ajouter des décorateurs de permission dans les vues.

## Intégration avec les autres modules

### Module Projets
- Les stocks sont liés aux projets
- Chaque projet peut avoir son propre stock

### Module Finances
- Les achats sont liés aux fournisseurs du module Finances
- Possibilité de créer des dépenses à partir des achats

### Module Personnel
- Traçabilité : qui a effectué quel mouvement
- Validation des achats par les responsables

## Améliorations futures possibles

1. **Rapports avancés**
   - Graphiques d'évolution des stocks
   - Analyse des coûts par projet
   - Prévisions de consommation

2. **Codes-barres**
   - Génération de codes-barres pour les produits
   - Scan pour les mouvements

3. **Inventaire physique**
   - Module d'inventaire avec écarts
   - Validation multi-niveaux

4. **Intégration comptable**
   - Export vers logiciels comptables
   - Valorisation FIFO/LIFO

5. **Notifications**
   - Email/SMS pour alertes de stock
   - Notifications aux responsables

## Support

Pour toute question ou problème, contactez l'équipe de développement.
