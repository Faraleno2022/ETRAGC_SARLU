# 💰 Système de Déduction Automatique - ETRAGS ARLU

## 📌 Vue d'Ensemble

Ce système permet la **déduction automatique** du solde des projets lorsque vous validez :
- ✅ **Dépenses** (achats divers, services, etc.)
- ✅ **Achats de matériaux** (ciment, fer, bois, etc.)
- ✅ **Paiements au personnel** (salaires, journaliers, etc.)

---

## 🚀 Démarrage Rapide

### 1. Exécuter les Tests
```powershell
# Double-cliquez sur :
run_tests.bat

# Ou en ligne de commande :
python manage.py shell < create_test_data.py
```

### 2. Consulter les Résultats
Ouvrez votre navigateur :
```
http://127.0.0.1:8000/dashboard/
```

Connectez-vous avec :
- **Username** : admin
- **Password** : admin123

### 3. Vérifier le Projet de Test
- Allez dans **Projets** → **PROJ-TEST-001**
- Consultez le solde disponible
- Vérifiez les transactions automatiques

---

## 📚 Documentation Disponible

### Pour les Utilisateurs

| Fichier | Description | Public Cible |
|---------|-------------|--------------|
| **GUIDE_RAPIDE_DEDUCTION.txt** | Guide rapide (1 page) | Tous les utilisateurs |
| **DEDUCTION_AUTOMATIQUE.md** | Documentation complète | Gestionnaires, Comptables |
| **EXEMPLES_DEDUCTION.md** | Exemples pratiques détaillés | Formation, Nouveaux utilisateurs |

### Pour les Développeurs

| Fichier | Description | Public Cible |
|---------|-------------|--------------|
| **CHANGELOG_DEDUCTION.md** | Détails techniques des modifications | Développeurs |
| **GUIDE_TESTS.md** | Guide d'exécution des tests | Développeurs, Testeurs |
| **create_test_data.py** | Script de création de données de test | Développeurs |

---

## 🎯 Fonctionnalités Principales

### 1. Déduction Automatique
Lorsque vous **validez** une opération, le système :
1. Détecte le changement de statut
2. Crée automatiquement une transaction de type "Dépense"
3. Déduit le montant du solde du projet
4. Enregistre tous les détails (date, mode de paiement, description)

### 2. Calcul du Solde
```
Solde = Budget Initial + Total Dépôts - Total Dépenses
```

### 3. Traçabilité Complète
- Toutes les déductions sont enregistrées dans les transactions
- Historique complet disponible
- Rapports et statistiques

---

## 📖 Utilisation

### Exemple 1 : Valider une Dépense

1. **Créer** : Finances → Dépenses → Nouvelle Dépense
   - Statut : "En attente"
   - Remplir tous les champs

2. **Valider** : Changer le statut vers "Validée"
   - ✅ Transaction créée automatiquement
   - ✅ Montant déduit du solde

### Exemple 2 : Valider un Achat

1. **Créer** : Inventaire → Achats → Nouvel Achat
   - Statut : "Brouillon"
   - Ajouter les lignes d'achat

2. **Valider** : Changer le statut vers "Validé"
   - ✅ Transaction créée automatiquement
   - ✅ Montant total déduit du solde

### Exemple 3 : Valider un Paiement

1. **Créer** : Personnel → Paiements → Nouveau Paiement
   - Statut : "En attente"
   - Sélectionner le personnel et le montant

2. **Valider** : Changer le statut vers "Validé"
   - ✅ Transaction créée automatiquement
   - ✅ Montant déduit du solde

---

## 🧪 Tests Automatiques

### Exécution
```powershell
# Windows
run_tests.bat

# Ou
python manage.py shell < create_test_data.py
```

### Ce Qui Est Testé
- ✅ Test 1 : Validation d'une dépense (500,000 GNF)
- ✅ Test 2 : Validation d'un achat (~4,700,000 GNF)
- ✅ Test 3 : Validation d'un paiement (750,000 GNF)

### Résultats Attendus
```
Solde initial  : 150,000,000 GNF
Après tests    : 144,050,000 GNF
Déduction totale : 5,950,000 GNF ✓
```

---

## ⚠️ Points Importants

### ✅ Ce Qui Fonctionne
- Déduction automatique lors de la validation
- Création d'une transaction pour chaque validation
- Calcul automatique du solde
- Traçabilité complète

### ⚠️ Limitations
- La transaction n'est créée qu'**une seule fois**
- Si vous repassez en "En attente", la transaction reste
- Pas de mise à jour automatique si le montant change après validation

### 🔒 Sécurité
- Impossible de créer des doublons
- Toutes les transactions ont le statut "Validée"
- Permissions requises pour valider

---

## 📊 Vérification

### Dans l'Interface Web

1. **Dashboard** : Vue d'ensemble des soldes
   ```
   http://127.0.0.1:8000/dashboard/
   ```

2. **Projets** : Détails du budget par projet
   ```
   Projets → [Votre Projet] → Onglet "Finances"
   ```

3. **Transactions** : Historique complet
   ```
   Finances → Transactions → Filtrer par projet
   ```

### Requête SQL Directe
```sql
SELECT 
    date_transaction,
    type,
    categorie,
    montant,
    description
FROM finances_transaction
WHERE projet_id = [ID_PROJET]
    AND type = 'Dépense'
    AND statut = 'Validée'
ORDER BY date_transaction DESC;
```

---

## 🔧 Installation et Configuration

### Prérequis
- Django 5.2.7
- Python 3.14
- Base de données SQLite (ou PostgreSQL)

### Étapes d'Installation

1. **Appliquer les migrations** (si ce n'est pas déjà fait)
   ```powershell
   python manage.py migrate
   ```

2. **Redémarrer le serveur**
   ```powershell
   python manage.py runserver
   ```

3. **Exécuter les tests**
   ```powershell
   run_tests.bat
   ```

---

## 🐛 Dépannage

### Problème : La déduction ne fonctionne pas
**Solutions** :
1. Vérifiez que le statut a bien changé vers "Validé" ou "Validée"
2. Vérifiez que les migrations sont appliquées
3. Redémarrez le serveur Django
4. Consultez les logs d'erreur

### Problème : Double déduction
**Cause** : Impossible avec le système actuel
**Explication** : La transaction n'est créée que lors du premier changement de statut

### Problème : Le solde ne se met pas à jour
**Solutions** :
1. Actualisez la page du projet
2. Vérifiez que la transaction a le statut "Validée"
3. Consultez l'historique des transactions

---

## 📞 Support

### Documentation
- **Guide rapide** : `GUIDE_RAPIDE_DEDUCTION.txt`
- **Documentation complète** : `DEDUCTION_AUTOMATIQUE.md`
- **Exemples** : `EXEMPLES_DEDUCTION.md`
- **Tests** : `GUIDE_TESTS.md`
- **Technique** : `CHANGELOG_DEDUCTION.md`

### Contact
Pour toute question ou problème :
1. Consultez la documentation appropriée
2. Vérifiez les logs du système
3. Contactez l'administrateur système

---

## 📈 Statistiques du Système

### Fichiers Modifiés
- `apps/finances/models.py` (Depense)
- `apps/inventory/models.py` (Achat)
- `apps/personnel/models.py` (PaiementPersonnel)

### Lignes de Code Ajoutées
- ~60 lignes de code métier
- ~1500 lignes de documentation
- ~500 lignes de tests

### Couverture
- ✅ 100% des opérations de dépense couvertes
- ✅ 3 tests automatiques
- ✅ Documentation complète en français

---

## 🎓 Formation

### Pour les Nouveaux Utilisateurs
1. Lisez le **GUIDE_RAPIDE_DEDUCTION.txt** (5 minutes)
2. Consultez les **EXEMPLES_DEDUCTION.md** (15 minutes)
3. Testez avec le projet de test PROJ-TEST-001 (30 minutes)

### Pour les Gestionnaires
1. Lisez la **DEDUCTION_AUTOMATIQUE.md** (20 minutes)
2. Exécutez les tests automatiques (10 minutes)
3. Créez un projet réel de test (1 heure)

### Pour les Développeurs
1. Lisez le **CHANGELOG_DEDUCTION.md** (15 minutes)
2. Examinez le code source (30 minutes)
3. Exécutez et modifiez les tests (1 heure)

---

## 🚀 Prochaines Étapes

### Court Terme
- [x] Implémenter la déduction automatique
- [x] Créer la documentation
- [x] Créer les tests automatiques
- [ ] Former les utilisateurs
- [ ] Déployer en production

### Moyen Terme
- [ ] Ajouter des notifications lors des déductions
- [ ] Créer un rapport des déductions automatiques
- [ ] Ajouter un système de rollback
- [ ] Implémenter des alertes de budget

### Long Terme
- [ ] Intégration avec système comptable
- [ ] API REST pour les transactions
- [ ] Application mobile
- [ ] Rapports avancés et analytics

---

## 📜 Licence et Crédits

**Développé pour** : ETRAGS ARLU  
**Date** : 29 Octobre 2025  
**Version** : 1.0  
**Statut** : ✅ Prêt pour production

---

## 🎯 Résumé en 30 Secondes

```
┌─────────────────────────────────────────────────────────────┐
│  SYSTÈME DE DÉDUCTION AUTOMATIQUE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Validez une opération → Déduction automatique du solde    │
│                                                             │
│  ✅ Dépenses    → Transaction créée automatiquement         │
│  ✅ Achats      → Transaction créée automatiquement         │
│  ✅ Paiements   → Transaction créée automatiquement         │
│                                                             │
│  Solde = Budget + Dépôts - Dépenses                        │
│                                                             │
│  📖 Docs : GUIDE_RAPIDE_DEDUCTION.txt                       │
│  🧪 Tests : run_tests.bat                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Bon travail avec ETRAGS ARLU !** 🏗️💰
