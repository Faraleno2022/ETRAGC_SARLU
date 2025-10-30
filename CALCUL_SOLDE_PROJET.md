# 💰 Calcul du Solde d'un Projet - Explication Détaillée

## 📊 Vue d'Ensemble

Le système calcule automatiquement le **solde disponible** de chaque projet en tenant compte de toutes les entrées et sorties d'argent.

---

## 🧮 Formule de Calcul

### Formule Principale
```
Solde Disponible = Budget Prévu + Total Dépôts - Total Retraits - Total Dépenses
```

### Décomposition
```
Montant Global = Budget Prévu + Total Dépôts
Solde Disponible = Montant Global - Total Retraits - Total Dépenses
```

---

## 📈 Composantes du Calcul

### 1. **Budget Prévu** (Montant Initial)
- C'est le budget initial défini lors de la création du projet
- Exemple : 100,000,000 GNF
- **Ne change jamais** après la création du projet

### 2. **Total Dépôts** (+)
- Somme de tous les dépôts reçus du client
- Type de transaction : "Dépôt"
- Statut : "Validée"
- **Augmente** le montant disponible

**Exemple** :
```
Dépôt 1 : +50,000,000 GNF
Dépôt 2 : +30,000,000 GNF
Total Dépôts : 80,000,000 GNF
```

### 3. **Total Retraits** (-)
- Somme de tous les retraits effectués
- Type de transaction : "Retrait"
- Statut : "Validée"
- **Diminue** le montant disponible

**Exemple** :
```
Retrait 1 : -5,000,000 GNF
Retrait 2 : -3,000,000 GNF
Total Retraits : 8,000,000 GNF
```

### 4. **Total Dépenses** (-)
- Somme de TOUTES les dépenses validées
- Type de transaction : "Dépense"
- Statut : "Validée"
- **Diminue** le montant disponible

Les dépenses incluent :
- ✅ **Achats de matériaux** (Catégorie: "Achat Matériaux")
- ✅ **Paiements du personnel** (Catégorie: "Paiement Personnel")
- ✅ **Autres dépenses** (Transport, Location, Services, etc.)

---

## 📊 Exemple Complet

### Situation Initiale
```
Projet : Villa Moderne à Kaloum
Code : PROJ-2025-001
```

### Étape 1 : Budget Initial
```
Budget Prévu : 100,000,000 GNF
─────────────────────────────
Solde : 100,000,000 GNF
```

### Étape 2 : Réception des Dépôts
```
Budget Prévu : 100,000,000 GNF
Dépôt 1      : +50,000,000 GNF
Dépôt 2      : +30,000,000 GNF
─────────────────────────────
Montant Global : 180,000,000 GNF
Solde : 180,000,000 GNF
```

### Étape 3 : Achats de Matériaux
```
Solde actuel : 180,000,000 GNF
Achat ciment : -12,400,000 GNF (Achat Matériaux)
Achat fer    : -11,900,000 GNF (Achat Matériaux)
─────────────────────────────
Total Achats : 24,300,000 GNF
Nouveau solde : 155,700,000 GNF
```

### Étape 4 : Paiements du Personnel
```
Solde actuel : 155,700,000 GNF
Chef chantier : -1,500,000 GNF (Paiement Personnel)
Maçons (5)    : -2,800,000 GNF (Paiement Personnel)
Ferrailleurs  : -1,470,000 GNF (Paiement Personnel)
─────────────────────────────
Total Paiements : 5,770,000 GNF
Nouveau solde : 149,930,000 GNF
```

### Étape 5 : Autres Dépenses
```
Solde actuel : 149,930,000 GNF
Location engins : -3,500,000 GNF (Transport)
Électricité    : -500,000 GNF (Services)
─────────────────────────────
Total Autres : 4,000,000 GNF
Nouveau solde : 145,930,000 GNF
```

### Résumé Final
```
Budget Prévu          : 100,000,000 GNF
Total Dépôts          : +80,000,000 GNF
─────────────────────────────────────
Montant Global        : 180,000,000 GNF

Total Retraits        : 0 GNF
Total Achats          : -24,300,000 GNF
Total Paiements       : -5,770,000 GNF
Total Autres Dépenses : -4,000,000 GNF
─────────────────────────────────────
Total Dépenses        : -34,070,000 GNF

SOLDE DISPONIBLE      : 145,930,000 GNF ✓
```

---

## 📱 Affichage dans le Dashboard

### Section Financière Globale

```
┌─────────────────────────────────────────────────┐
│         FINANCES GLOBALES (Tous Projets)        │
├─────────────────────────────────────────────────┤
│                                                 │
│  Budget Prévu Total    : 100,000,000 GNF       │
│  Total Dépôts          : +80,000,000 GNF       │
│  ─────────────────────────────────────────     │
│  Montant Global        : 180,000,000 GNF       │
│                                                 │
│  Total Retraits        : -0 GNF                │
│  Total Dépenses        : -34,070,000 GNF       │
│  ─────────────────────────────────────────     │
│  SOLDE DISPONIBLE      : 145,930,000 GNF ✓     │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Détail des Dépenses

```
┌─────────────────────────────────────────────────┐
│            DÉTAIL DES DÉPENSES                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Achats Matériaux      : 24,300,000 GNF (71%)  │
│  Paiements Personnel   : 5,770,000 GNF  (17%)  │
│  Autres Dépenses       : 4,000,000 GNF  (12%)  │
│  ─────────────────────────────────────────     │
│  TOTAL DÉPENSES        : 34,070,000 GNF        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔍 Vérification du Calcul

### Méthode 1 : Via l'Interface Web
1. Accédez au Dashboard : `http://127.0.0.1:8000/dashboard/`
2. Consultez la section "Finances Globales"
3. Vérifiez chaque montant affiché

### Méthode 2 : Via le Détail du Projet
1. Allez dans **Projets** → Sélectionnez votre projet
2. Consultez l'onglet **"Finances"** ou **"Budget"**
3. Vous verrez :
   - Budget prévu
   - Total dépôts
   - Total dépenses (détaillé)
   - Solde disponible

### Méthode 3 : Via les Transactions
1. Allez dans **Finances** → **Transactions**
2. Filtrez par projet
3. Vérifiez manuellement :
   - Somme des dépôts
   - Somme des retraits
   - Somme des dépenses

---

## 📊 Indicateurs Calculés

### 1. Pourcentage du Budget Consommé
```
% Consommé = (Total Dépenses / Montant Global) × 100
```

**Exemple** :
```
Total Dépenses : 34,070,000 GNF
Montant Global : 180,000,000 GNF
% Consommé = (34,070,000 / 180,000,000) × 100 = 18.9%
```

### 2. Budget Dépassé ?
```
Budget Dépassé = Solde Disponible < 0
```

**Exemple** :
```
Solde : 145,930,000 GNF > 0
Budget Dépassé : NON ✓
```

### 3. Taux d'Utilisation
```
Taux = (Total Dépenses / Montant Global) × 100
```

---

## ⚠️ Points Importants

### ✅ Ce Qui Est Compté
- ✅ Toutes les transactions avec statut **"Validée"**
- ✅ Achats de matériaux validés
- ✅ Paiements du personnel validés
- ✅ Dépenses diverses validées
- ✅ Dépôts reçus
- ✅ Retraits effectués

### ❌ Ce Qui N'Est PAS Compté
- ❌ Transactions en attente
- ❌ Transactions rejetées
- ❌ Achats en brouillon
- ❌ Paiements non validés
- ❌ Dépenses en attente

### 🔄 Mise à Jour Automatique
Le solde est recalculé **automatiquement** :
- Lors de la validation d'une dépense
- Lors de la validation d'un achat
- Lors de la validation d'un paiement
- Lors de l'ajout d'un dépôt
- Lors de l'ajout d'un retrait

---

## 🎯 Cas d'Usage

### Cas 1 : Vérifier si on peut faire un achat
```
Question : Puis-je acheter pour 10,000,000 GNF ?
Solde actuel : 145,930,000 GNF
Réponse : OUI ✓ (Solde suffisant)
```

### Cas 2 : Calculer le budget restant
```
Budget total : 180,000,000 GNF
Dépensé : 34,070,000 GNF
Restant : 145,930,000 GNF
% Restant : 81.1%
```

### Cas 3 : Prévoir les dépenses futures
```
Solde actuel : 145,930,000 GNF
Dépenses prévues :
  - Peinture : 15,000,000 GNF
  - Plomberie : 8,000,000 GNF
  - Électricité : 12,000,000 GNF
Total prévu : 35,000,000 GNF

Solde après : 145,930,000 - 35,000,000 = 110,930,000 GNF ✓
```

---

## 🔧 Code de Calcul

### Dans le Modèle Projet
```python
def get_budget_disponible(self):
    """Retourne le budget disponible"""
    return self.montant_prevu + self.get_total_depots() - self.get_total_depenses()

def get_total_depots(self):
    """Retourne le total des dépôts"""
    return Transaction.objects.filter(
        projet=self,
        type='Dépôt',
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0

def get_total_depenses(self):
    """Retourne le total des dépenses"""
    return Transaction.objects.filter(
        projet=self,
        type__in=['Dépense', 'Retrait'],
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
```

### Dans la Vue Dashboard
```python
# Budget prévu total
budget_prevu_total = Projet.objects.aggregate(
    total=Sum('montant_prevu')
)['total'] or 0

# Total dépôts
total_depots = Transaction.objects.filter(
    type='Dépôt',
    statut='Validée'
).aggregate(total=Sum('montant'))['total'] or 0

# Total dépenses
total_depenses = Transaction.objects.filter(
    type='Dépense',
    statut='Validée'
).aggregate(total=Sum('montant'))['total'] or 0

# Calcul du solde
montant_global = budget_prevu_total + total_depots
solde_disponible = montant_global - total_retraits - total_depenses
```

---

## 📞 Support

Pour toute question sur le calcul du solde :
1. Consultez ce document
2. Vérifiez les transactions dans l'interface
3. Consultez `DEDUCTION_AUTOMATIQUE.md`
4. Contactez l'administrateur si nécessaire

---

**Date** : 29 Octobre 2025  
**Version** : 1.0  
**Statut** : ✅ Documentation complète
