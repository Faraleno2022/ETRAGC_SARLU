# Module de Gestion de Stock - Guide d'Installation et d'Utilisation

## 📦 Vue d'ensemble

Le module de gestion de stock a été créé avec succès pour votre application ETRAGC SARLU. Il permet de :

- ✅ Gérer les produits et matériaux de construction
- ✅ Suivre les stocks par projet
- ✅ Enregistrer les achats auprès des fournisseurs
- ✅ Tracer tous les mouvements de stock (entrées/sorties/transferts)
- ✅ Recevoir des alertes pour les stocks faibles
- ✅ Calculer automatiquement les valeurs de stock

## 🚀 Installation

### Étape 1 : Appliquer les migrations

```bash
python manage.py migrate
```

Cette commande va créer toutes les tables nécessaires dans la base de données.

### Étape 2 : Charger les données initiales

Vous avez deux options :

**Option A : Via le script Python (recommandé)**
```bash
python init_inventory.py
```

**Option B : Via les fixtures Django**
```bash
python manage.py loaddata apps/inventory/fixtures/initial_data.json
```

Cela créera :
- 8 unités de mesure (kg, m, m², m³, pièce, litre, sac, tonne)
- 10 catégories de produits (Ciment, Fer, Bois, Peinture, etc.)

### Étape 3 : Démarrer le serveur

```bash
python manage.py runserver
```

Accédez au module via : **http://localhost:8000/inventory/**

## 📋 Structure du Module

### Modèles créés

1. **UniteMessure** - Unités de mesure (kg, m, pièce, etc.)
2. **CategorieProduit** - Catégories de produits
3. **Produit** - Produits/matériaux avec code auto-généré
4. **Stock** - Stock par projet avec quantité et valeur
5. **Achat** - Bons d'achat avec numéro auto-généré
6. **LigneAchat** - Détail des produits achetés
7. **MouvementStock** - Historique de tous les mouvements

### Pages disponibles

- **Dashboard** : `/inventory/` - Vue d'ensemble avec statistiques
- **Produits** : `/inventory/produits/` - Liste et gestion des produits
- **Stocks** : `/inventory/stocks/` - Vue des stocks par projet
- **Achats** : `/inventory/achats/` - Gestion des achats
- **Mouvements** : `/inventory/mouvements/` - Historique des mouvements
- **Alertes** : `/inventory/alertes/` - Alertes de stock faible

## 💡 Utilisation

### 1. Créer des produits

1. Allez dans **Stock → Produits**
2. Cliquez sur **Nouveau produit**
3. Remplissez les informations :
   - Nom du produit
   - Catégorie
   - Unité de mesure
   - Prix unitaire moyen
   - Stock minimum (seuil d'alerte)

### 2. Effectuer un achat

1. Allez dans **Stock → Achats**
2. Cliquez sur **Nouvel achat**
3. Sélectionnez :
   - Le projet
   - Le fournisseur
   - Date d'achat
   - Mode de paiement
4. Ajoutez les lignes d'achat (produits)
5. Enregistrez en **Brouillon**
6. **Validez** l'achat quand il est confirmé
7. **Marquez comme reçu** quand les produits arrivent
   - ⚠️ Les stocks seront automatiquement mis à jour

### 3. Gérer les mouvements de stock

**Types de mouvements :**

- **Entrée** : Ajout de produits (réception, retour)
- **Sortie** : Retrait de produits (utilisation sur chantier)
- **Ajustement** : Correction après inventaire
- **Transfert** : Déplacement entre projets

**Pour créer un mouvement :**
1. Allez dans **Stock → Mouvements**
2. Cliquez sur **Nouveau mouvement**
3. Sélectionnez le stock à modifier
4. Choisissez le type de mouvement
5. Indiquez la quantité et le motif

### 4. Surveiller les alertes

- Le dashboard affiche les stocks faibles
- Page dédiée : **Stock → Alertes**
- Les stocks en dessous du minimum sont marqués en rouge
- Vous pouvez commander directement depuis les alertes

## 🔧 Fonctionnalités avancées

### Calculs automatiques

- **Prix unitaire moyen** : Mis à jour à chaque réception d'achat
- **Valeur du stock** : Quantité × Prix unitaire moyen
- **Montant total achat** : Somme des lignes d'achat

### Workflow des achats

```
Brouillon → Validé → Reçu
   ↓          ↓        ↓
Éditable  Confirmé  Stocks mis à jour
```

### Traçabilité

- Tous les mouvements sont enregistrés
- Historique complet par stock
- Quantités avant/après chaque mouvement
- Utilisateur ayant effectué l'action

## 📊 Rapports et Statistiques

Le dashboard affiche :
- Nombre total de produits
- Nombre de stocks actifs
- Valeur totale du stock
- Nombre d'alertes
- Achats récents
- Mouvements récents
- Top 5 projets par valeur de stock

## 🔐 Sécurité

- Authentification requise pour accéder au module
- Traçabilité de toutes les actions
- Validation des quantités (pas de stock négatif)
- Pièces justificatives pour les achats

## 🎨 Interface

- Design moderne et responsive
- Navigation intuitive
- Badges de statut colorés
- Alertes visuelles pour stocks faibles
- Filtres et recherche sur toutes les listes

## 📝 Exemples de produits à créer

### Ciment et Liants
- Ciment CPJ 42.5 (sac de 50kg)
- Chaux hydraulique
- Mortier prêt à l'emploi

### Agrégats
- Sable fin (m³)
- Gravier 5/15 (m³)
- Tout-venant (m³)

### Fer et Acier
- Fer à béton Ø8 (kg)
- Fer à béton Ø10 (kg)
- Treillis soudé (m²)

### Bois
- Planche 27x200 (m)
- Chevron 63x75 (m)
- Contreplaqué 18mm (m²)

## 🆘 Dépannage

### Les migrations ne s'appliquent pas
```bash
python manage.py makemigrations inventory
python manage.py migrate inventory
```

### Erreur "No module named inventory"
Vérifiez que `'apps.inventory'` est dans `INSTALLED_APPS` dans `config/settings.py`

### Les données initiales ne se chargent pas
```bash
python init_inventory.py
```

### Le module n'apparaît pas dans la navigation
Videz le cache du navigateur (Ctrl+F5)

## 📞 Support

Pour toute question ou problème :
1. Consultez le fichier `apps/inventory/README.md`
2. Vérifiez les logs Django
3. Contactez l'équipe de développement

## 🎯 Prochaines étapes

1. ✅ Appliquer les migrations
2. ✅ Charger les données initiales
3. ✅ Créer vos premiers produits
4. ✅ Configurer les stocks minimum
5. ✅ Effectuer votre premier achat
6. ✅ Tester les mouvements de stock

---

**Module développé pour ETRAGC SARLU**
*Gestion complète de stock pour projets de construction*
