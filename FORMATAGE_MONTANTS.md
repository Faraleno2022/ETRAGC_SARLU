# Configuration du Formatage Automatique des Montants

## 📋 Vue d'ensemble

Le système de formatage automatique des montants a été configuré pour faciliter la lecture et la saisie des montants dans toute l'application.

## ✅ Champs concernés

### 1. **Facturation (Invoicing)**
- ✅ Devis
  - Montant HT (lecture seule, calculé automatiquement)
  - Prix unitaire HT (lignes de devis)
  
- ✅ Factures
  - Montant HT (lecture seule, calculé automatiquement)
  - Prix unitaire HT (lignes de facture)
  
- ✅ Paiements de factures
  - Montant du paiement

### 2. **Finances**
- ✅ Transactions
  - Montant de la transaction
  
- ✅ Dépenses
  - Montant de la dépense

### 3. **Personnel**
- ✅ Personnel
  - Salaire journalier
  
- ✅ Paiements du personnel
  - Montant du paiement

### 4. **Projets**
- ✅ Projets
  - Montant prévu

## 🎨 Fonctionnalités

### Formatage automatique
- **Espacement tous les 3 chiffres** : `1000000` devient `1 000 000`
- **Formatage en temps réel** pendant la saisie
- **Conservation de la position du curseur** lors du formatage
- **Support des décimales** : `1000000.50` devient `1 000 000.50`

### Style visuel
- **Police monospace** pour une meilleure lisibilité
- **Alignement à droite** pour les montants
- **Indicateur GNF** visible sur certains champs
- **Couleur de fond différente** pour les champs en lecture seule
- **Animation au focus** pour indiquer le champ actif

## 🔧 Implémentation technique

### Fichiers créés
1. **`static/js/money-formatter.js`**
   - Script JavaScript pour le formatage automatique
   - Fonctions utilitaires : `formatMoney()`, `parseMoney()`
   - Nettoyage automatique avant soumission du formulaire

2. **`static/css/money-input.css`**
   - Styles CSS pour les champs de montants
   - Classes : `.money-input`, `.money-input-wrapper`
   - Animations et transitions

### Formulaires modifiés
- ✅ `apps/invoicing/forms.py`
- ✅ `apps/finances/forms.py`
- ✅ `apps/personnel/forms.py`
- ✅ `apps/projects/forms.py`

### Template de base
- ✅ `templates/base/base.html` - Inclusion des fichiers CSS et JS

## 💡 Utilisation

### Pour les développeurs
Pour ajouter le formatage à un nouveau champ de montant :

```python
# Dans votre formulaire
widgets = {
    'montant': forms.NumberInput(attrs={
        'class': 'form-control money-input',
        'step': '0.01'
    }),
}
```

### Fonctions JavaScript disponibles

```javascript
// Formater un nombre pour l'affichage
let formatted = formatMoney(1000000, 0);  // "1 000 000"
let formattedWithDecimals = formatMoney(1000000.50, 2);  // "1 000 000.50"

// Parser un montant formaté
let amount = parseMoney("1 000 000");  // 1000000
```

## 📱 Responsive

Le formatage fonctionne sur tous les appareils :
- 💻 Desktop
- 📱 Mobile
- 📲 Tablette

## 🎯 Avantages

1. **Meilleure lisibilité** - Les grands montants sont plus faciles à lire
2. **Moins d'erreurs** - Visualisation claire des montants saisis
3. **Expérience utilisateur améliorée** - Formatage automatique en temps réel
4. **Cohérence** - Tous les champs de montants ont le même comportement
5. **Performance** - Pas d'impact sur les performances de l'application

## 🔍 Exemples de formatage

| Saisie | Affichage |
|--------|-----------|
| 1000 | 1 000 |
| 50000 | 50 000 |
| 1000000 | 1 000 000 |
| 2500000.50 | 2 500 000.50 |
| 15000000 | 15 000 000 |

## 🚀 Déploiement

Les fichiers statiques ont été collectés avec :
```bash
python manage.py collectstatic --noinput
```

## ⚠️ Notes importantes

1. Les valeurs sont **automatiquement nettoyées** (espaces retirés) avant la soumission du formulaire
2. Les champs en **lecture seule** (readonly) ne sont pas formatés lors de la saisie mais peuvent afficher le formatage
3. Le formatage fonctionne avec les **virgules et les points** comme séparateurs décimaux
4. Compatible avec tous les navigateurs modernes

## 📝 Maintenance

Pour désactiver le formatage sur un champ spécifique, retirez simplement la classe `money-input` :

```python
'montant': forms.NumberInput(attrs={
    'class': 'form-control',  # Sans 'money-input'
    'step': '0.01'
}),
```

---

**Date de mise en œuvre** : 26 octobre 2025  
**Version** : 1.0  
**Statut** : ✅ Actif
