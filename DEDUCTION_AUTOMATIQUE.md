# 💰 Système de Déduction Automatique du Solde des Projets

## 📌 Vue d'ensemble

Le système déduit **automatiquement** le solde de chaque projet lorsque vous validez :
- ✅ Des **dépenses** (achats divers, services, etc.)
- ✅ Des **achats de matériaux** (ciment, fer, bois, etc.)
- ✅ Des **paiements au personnel** (salaires, journaliers, etc.)

## 🔄 Comment ça fonctionne

### 1️⃣ Dépenses (Module Finances)

**Chemin** : Finances → Dépenses → Créer/Modifier une dépense

**Processus** :
1. Créez une dépense avec le statut **"En attente"**
2. Remplissez tous les détails (montant, catégorie, fournisseur, etc.)
3. Lorsque vous changez le statut vers **"Validée"** :
   - ✅ Une transaction de type "Dépense" est automatiquement créée
   - ✅ Le montant est **déduit du solde du projet**
   - ✅ La transaction apparaît dans l'historique des transactions

**Exemple** :
```
Dépense : Achat de peinture - 500,000 GNF
Statut : En attente → Validée
Résultat : -500,000 GNF du solde du projet
```

---

### 2️⃣ Achats de Matériaux (Module Inventaire)

**Chemin** : Inventaire → Achats → Créer/Modifier un achat

**Processus** :
1. Créez un achat avec le statut **"Brouillon"**
2. Ajoutez les lignes d'achat (produits, quantités, prix)
3. Lorsque vous changez le statut vers **"Validé"** ou **"Reçu"** :
   - ✅ Une transaction de type "Dépense" est automatiquement créée
   - ✅ Catégorie : "Achat Matériaux"
   - ✅ Le montant total est **déduit du solde du projet**
   - ✅ Le stock est mis à jour (si statut = "Reçu")

**Exemple** :
```
Achat : 50 sacs de ciment - 2,500,000 GNF
Statut : Brouillon → Validé
Résultat : -2,500,000 GNF du solde du projet
```

---

### 3️⃣ Paiements du Personnel (Module Personnel)

**Chemin** : Personnel → Paiements → Créer/Modifier un paiement

**Processus** :
1. Créez un paiement avec le statut **"En attente"**
2. Sélectionnez le personnel, le projet, et le montant
3. Lorsque vous changez le statut vers **"Validé"** :
   - ✅ Une transaction de type "Dépense" est automatiquement créée
   - ✅ Catégorie : "Paiement Personnel"
   - ✅ Le montant est **déduit du solde du projet**
   - ✅ Le paiement est enregistré dans l'historique du personnel

**Exemple** :
```
Paiement : Salaire Mamadou Diallo - 1,200,000 GNF
Statut : En attente → Validé
Résultat : -1,200,000 GNF du solde du projet
```

---

## 📊 Calcul du Solde du Projet

Le solde d'un projet est calculé comme suit :

```
Solde = Budget Initial + Total Dépôts - Total Dépenses
```

**Où** :
- **Budget Initial** : Montant prévu du projet (montant_prevu)
- **Total Dépôts** : Somme de toutes les transactions de type "Dépôt" validées
- **Total Dépenses** : Somme de toutes les transactions de type "Dépense" et "Retrait" validées

---

## ⚠️ Points Importants

### ✅ Ce qui se passe automatiquement :
- La création d'une transaction de dépense
- La déduction du montant du solde du projet
- L'enregistrement de tous les détails (date, mode de paiement, description)

### ❌ Ce qui ne se passe PAS automatiquement :
- **Suppression de transaction** : Si vous repassez un élément en "En attente", la transaction déjà créée reste
- **Modification de montant** : Si vous modifiez le montant après validation, la transaction initiale n'est pas mise à jour

### 🔒 Sécurité :
- Les transactions sont créées **une seule fois** lors du changement de statut
- Impossible de créer des doublons pour la même validation
- Toutes les transactions ont le statut **"Validée"** pour être comptabilisées

---

## 📈 Suivi et Vérification

### Vérifier les transactions créées :
1. Allez dans **Finances → Transactions**
2. Filtrez par projet
3. Vous verrez toutes les transactions automatiques avec :
   - Type : "Dépense"
   - Catégorie : "Achat Matériaux", "Paiement Personnel", ou le nom de la catégorie de dépense
   - Description : Détails de l'opération

### Consulter le solde du projet :
1. Allez dans **Projets → Détail du projet**
2. Consultez la section "Budget et Finances"
3. Vous verrez :
   - Budget initial
   - Total des dépôts
   - Total des dépenses
   - **Solde disponible**

---

## 🎯 Workflow Recommandé

### Pour une dépense :
1. **Créer** la dépense (statut : En attente)
2. **Vérifier** les informations
3. **Valider** la dépense → Déduction automatique ✅

### Pour un achat :
1. **Créer** l'achat (statut : Brouillon)
2. **Ajouter** les lignes d'achat
3. **Valider** l'achat → Déduction automatique ✅
4. **Marquer comme reçu** → Mise à jour du stock ✅

### Pour un paiement personnel :
1. **Créer** le paiement (statut : En attente)
2. **Vérifier** le montant et les jours travaillés
3. **Valider** le paiement → Déduction automatique ✅

---

## 🛠️ Dépannage

### Problème : La déduction ne fonctionne pas
**Solutions** :
- Vérifiez que le statut a bien changé vers "Validé" ou "Validée"
- Vérifiez que l'élément n'était pas déjà validé auparavant
- Consultez les transactions pour voir si elle a été créée

### Problème : Double déduction
**Cause** : Impossible avec le système actuel
**Explication** : La transaction n'est créée que si le statut change d'un état non-validé vers validé

### Problème : Le solde ne se met pas à jour
**Solutions** :
- Actualisez la page du projet
- Vérifiez que la transaction a le statut "Validée"
- Redémarrez le serveur Django si nécessaire

---

## 📞 Support

Pour toute question ou problème :
1. Consultez l'historique des transactions du projet
2. Vérifiez les logs du système
3. Contactez l'administrateur système

---

**Date de mise à jour** : 29 Octobre 2025  
**Version** : 1.0
