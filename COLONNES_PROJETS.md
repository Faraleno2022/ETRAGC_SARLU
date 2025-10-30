# 📊 Nouvelles Colonnes dans la Liste des Projets

## 🎯 Vue d'Ensemble

La liste des projets affiche maintenant **3 colonnes financières** qui se mettent à jour automatiquement :

1. **Budget Prévu** - Budget initial + Dépôts reçus
2. **Montant Dépensé** - Total de toutes les dépenses validées
3. **Montant Disponible** - Solde restant après déductions

---

## 📋 Structure du Tableau

### Colonnes Affichées

```
┌────────┬──────────────┬─────────┬────────────────┬─────────────────┬────────────────────┬────────┬────────────┬─────────┐
│ Code   │ Nom du Projet│ Client  │ Budget Prévu   │ Montant Dépensé │ Montant Disponible │ Statut │ Avancement │ Actions │
├────────┼──────────────┼─────────┼────────────────┼─────────────────┼────────────────────┼────────┼────────────┼─────────┤
│ PROJ-  │ Villa        │ DIALLO  │ Budget: 100M   │ 34,070,000 GNF  │ 145,930,000 GNF   │ En     │ ████░░ 45% │ 👁️ ✏️   │
│ 2025-  │ Moderne      │ Mamadou │ +Dépôts: 80M   │ ▓▓░░░░░░░░ 19%  │ ✓                 │ cours  │            │         │
│ 001    │              │         │ 180,000,000    │ dépensé         │                    │        │            │         │
└────────┴──────────────┴─────────┴────────────────┴─────────────────┴────────────────────┴────────┴────────────┴─────────┘
```

---

## 💰 Colonne 1 : Budget Prévu

### Affichage
```
Budget: 100,000,000 GNF      (gris, petit)
+Dépôts: 80,000,000 GNF      (vert, petit, si > 0)
180,000,000 GNF              (bleu, gras, TOTAL)
```

### Calcul
```
Montant Global = Budget Initial + Total Dépôts
```

### Mise à Jour Automatique
- ✅ **Augmente** quand vous ajoutez un dépôt
- ✅ Le budget initial ne change jamais
- ✅ Seuls les dépôts validés sont comptés

### Exemple
```
Situation initiale :
  Budget: 100,000,000 GNF
  Total: 100,000,000 GNF

Après dépôt de 50,000,000 GNF :
  Budget: 100,000,000 GNF
  +Dépôts: 50,000,000 GNF
  Total: 150,000,000 GNF ✓

Après 2ème dépôt de 30,000,000 GNF :
  Budget: 100,000,000 GNF
  +Dépôts: 80,000,000 GNF
  Total: 180,000,000 GNF ✓
```

---

## 📉 Colonne 2 : Montant Dépensé

### Affichage
```
34,070,000 GNF               (badge rouge)
▓▓░░░░░░░░                   (barre de progression rouge)
19% dépensé                  (petit texte gris)
```

### Calcul
```
Total Dépensé = Somme de toutes les transactions de type "Dépense" et "Retrait" validées
```

### Inclut
- ✅ **Achats de matériaux** (ciment, fer, sable, etc.)
- ✅ **Paiements du personnel** (salaires, journaliers)
- ✅ **Autres dépenses** (transport, location, services)
- ✅ **Retraits** effectués

### Mise à Jour Automatique
- ✅ **Augmente** quand vous validez une dépense
- ✅ **Augmente** quand vous validez un achat
- ✅ **Augmente** quand vous validez un paiement personnel
- ✅ **Augmente** quand vous effectuez un retrait

### Exemple
```
Situation initiale :
  Montant dépensé: 0 GNF
  0% dépensé

Après achat de matériaux (12,000,000 GNF) :
  Montant dépensé: 12,000,000 GNF
  7% dépensé ✓

Après paiement personnel (5,000,000 GNF) :
  Montant dépensé: 17,000,000 GNF
  9% dépensé ✓

Après dépense transport (3,000,000 GNF) :
  Montant dépensé: 20,000,000 GNF
  11% dépensé ✓
```

---

## 💵 Colonne 3 : Montant Disponible

### Affichage avec Indicateurs de Couleur

#### ✅ Solde Normal (Vert)
```
145,930,000 GNF              (badge vert)
```
- Solde > 10% du montant global
- Situation normale
- Pas d'alerte

#### ⚠️ Solde Faible (Orange)
```
15,000,000 GNF               (badge orange)
Solde faible                 (texte orange)
```
- Solde < 10% du montant global
- Attention requise
- Prévoir un dépôt

#### ❌ Budget Dépassé (Rouge)
```
⚠️ -5,000,000 GNF            (badge rouge avec icône)
Budget dépassé!              (texte rouge)
```
- Solde négatif
- Budget dépassé
- Action urgente requise

### Calcul
```
Solde Disponible = Budget Prévu + Dépôts - Retraits - Dépenses
```

### Mise à Jour Automatique
- ✅ **Augmente** quand vous ajoutez un dépôt
- ✅ **Diminue** quand vous validez une dépense
- ✅ **Diminue** quand vous validez un achat
- ✅ **Diminue** quand vous validez un paiement
- ✅ **Diminue** quand vous effectuez un retrait

### Exemple Complet
```
Budget initial: 100,000,000 GNF
Dépôt: +80,000,000 GNF
─────────────────────────────
Montant global: 180,000,000 GNF
Solde: 180,000,000 GNF ✓ (Vert)

Achat matériaux: -24,300,000 GNF
Solde: 155,700,000 GNF ✓ (Vert)

Paiements personnel: -5,770,000 GNF
Solde: 149,930,000 GNF ✓ (Vert)

Autres dépenses: -4,000,000 GNF
Solde: 145,930,000 GNF ✓ (Vert)

... plus de dépenses ...

Solde: 15,000,000 GNF ⚠️ (Orange - Solde faible)

... encore plus de dépenses ...

Solde: -5,000,000 GNF ❌ (Rouge - Budget dépassé!)
```

---

## 🔄 Mise à Jour Automatique

### Quand les Colonnes Se Mettent à Jour

#### 1. Ajout d'un Dépôt
```
Action : Finances → Transactions → Nouveau Dépôt → Valider
Effet :
  ✓ Budget Prévu : AUGMENTE
  - Montant Dépensé : Inchangé
  ✓ Montant Disponible : AUGMENTE
```

#### 2. Validation d'un Achat
```
Action : Inventaire → Achats → Valider un achat
Effet :
  - Budget Prévu : Inchangé
  ✓ Montant Dépensé : AUGMENTE
  ✓ Montant Disponible : DIMINUE
```

#### 3. Validation d'un Paiement Personnel
```
Action : Personnel → Paiements → Valider un paiement
Effet :
  - Budget Prévu : Inchangé
  ✓ Montant Dépensé : AUGMENTE
  ✓ Montant Disponible : DIMINUE
```

#### 4. Validation d'une Dépense
```
Action : Finances → Dépenses → Valider une dépense
Effet :
  - Budget Prévu : Inchangé
  ✓ Montant Dépensé : AUGMENTE
  ✓ Montant Disponible : DIMINUE
```

#### 5. Effectuer un Retrait
```
Action : Finances → Transactions → Nouveau Retrait → Valider
Effet :
  - Budget Prévu : Inchangé
  ✓ Montant Dépensé : AUGMENTE
  ✓ Montant Disponible : DIMINUE
```

---

## 📊 Exemple Visuel Complet

### Projet 1 : Villa Moderne (Situation Normale)
```
┌─────────────────────────────────────────────────────────────────────┐
│ Code: PROJ-2025-001                                                 │
│ Nom: Villa Moderne à Kaloum                                         │
│ Client: DIALLO Mamadou                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Budget Prévu:                                                       │
│   Budget: 100,000,000 GNF                                          │
│   +Dépôts: 80,000,000 GNF                                          │
│   Total: 180,000,000 GNF                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Montant Dépensé:                                                    │
│   34,070,000 GNF (badge rouge)                                     │
│   ▓▓░░░░░░░░ 19% dépensé                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Montant Disponible:                                                 │
│   145,930,000 GNF ✓ (badge vert)                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Projet 2 : Immeuble Commercial (Solde Faible)
```
┌─────────────────────────────────────────────────────────────────────┐
│ Code: PROJ-2025-002                                                 │
│ Nom: Immeuble Commercial                                            │
│ Client: CAMARA Ibrahima                                             │
├─────────────────────────────────────────────────────────────────────┤
│ Budget Prévu:                                                       │
│   Budget: 500,000,000 GNF                                          │
│   +Dépôts: 200,000,000 GNF                                         │
│   Total: 700,000,000 GNF                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Montant Dépensé:                                                    │
│   665,000,000 GNF (badge rouge)                                    │
│   ▓▓▓▓▓▓▓▓▓░ 95% dépensé                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Montant Disponible:                                                 │
│   35,000,000 GNF ⚠️ (badge orange)                                  │
│   Solde faible                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Projet 3 : Rénovation Maison (Budget Dépassé)
```
┌─────────────────────────────────────────────────────────────────────┐
│ Code: PROJ-2025-003                                                 │
│ Nom: Rénovation Maison                                              │
│ Client: SOW Amadou                                                  │
├─────────────────────────────────────────────────────────────────────┤
│ Budget Prévu:                                                       │
│   Budget: 50,000,000 GNF                                           │
│   +Dépôts: 30,000,000 GNF                                          │
│   Total: 80,000,000 GNF                                            │
├─────────────────────────────────────────────────────────────────────┤
│ Montant Dépensé:                                                    │
│   85,000,000 GNF (badge rouge)                                     │
│   ▓▓▓▓▓▓▓▓▓▓ 106% dépensé                                          │
├─────────────────────────────────────────────────────────────────────┤
│ Montant Disponible:                                                 │
│   ⚠️ -5,000,000 GNF ❌ (badge rouge)                                │
│   Budget dépassé!                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Codes Couleur

### Budget Prévu
- **Gris** : Budget initial
- **Vert** : Dépôts (si > 0)
- **Bleu gras** : Total

### Montant Dépensé
- **Badge rouge** : Montant total dépensé
- **Barre rouge** : Pourcentage de consommation
- **Texte gris** : Pourcentage en texte

### Montant Disponible
- **Badge vert** : Solde normal (> 10%)
- **Badge orange** : Solde faible (< 10%)
- **Badge rouge** : Budget dépassé (< 0)

---

## 📱 Responsive Design

Le tableau s'adapte automatiquement à la taille de l'écran :
- **Desktop** : Toutes les colonnes visibles
- **Tablette** : Scroll horizontal disponible
- **Mobile** : Scroll horizontal avec colonnes prioritaires

---

## 🔍 Utilisation

### Consulter les Détails
1. Cliquez sur le **code du projet** ou l'icône 👁️
2. Accédez à la page de détails
3. Consultez l'onglet "Finances" pour plus d'informations

### Filtrer les Projets
- Par **statut** : Tous, En cours, Terminé, etc.
- Par **recherche** : Code, nom, client

### Exporter les Données
- **Excel** : Bouton vert en haut à droite
- **PDF** : Bouton rouge en haut à droite

---

## ⚠️ Points Importants

### ✅ Avantages
- Visibilité immédiate de la situation financière
- Alertes visuelles (couleurs)
- Mise à jour automatique en temps réel
- Pas besoin d'ouvrir chaque projet

### 🔄 Mise à Jour
- Les montants se recalculent à chaque chargement de la page
- Basés sur les transactions validées uniquement
- Synchronisés avec le système de déduction automatique

### 📊 Précision
- Les calculs utilisent les mêmes méthodes que le dashboard
- Cohérence garantie avec les détails du projet
- Basés sur les transactions de la base de données

---

## 🎯 Cas d'Usage

### Cas 1 : Identifier les Projets en Difficulté
```
Recherchez les badges rouges ou oranges
→ Budget dépassé ou solde faible
→ Action requise
```

### Cas 2 : Vérifier la Disponibilité Budgétaire
```
Consultez la colonne "Montant Disponible"
→ Solde vert = OK pour nouvelles dépenses
→ Solde orange = Attention
→ Solde rouge = Besoin de dépôt
```

### Cas 3 : Suivre la Consommation
```
Consultez la barre de progression dans "Montant Dépensé"
→ Visualisation rapide du % consommé
→ Comparaison entre projets
```

---

## 📞 Support

Pour toute question :
1. Consultez `CALCUL_SOLDE_PROJET.md` pour les détails des calculs
2. Consultez `DEDUCTION_AUTOMATIQUE.md` pour le système de déduction
3. Contactez l'administrateur si nécessaire

---

**Date** : 30 Octobre 2025  
**Version** : 1.0  
**Statut** : ✅ Fonctionnel
