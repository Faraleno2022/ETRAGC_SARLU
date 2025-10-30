# 🧪 Guide d'Exécution des Tests

## 📋 Objectif

Ce guide explique comment exécuter les tests automatiques pour vérifier que le système de déduction automatique fonctionne correctement.

---

## 🚀 Méthode 1 : Exécution Rapide (Recommandée)

### Windows
Double-cliquez sur le fichier :
```
run_tests.bat
```

Le script va :
1. Créer toutes les données de test nécessaires
2. Exécuter 3 tests automatiques
3. Afficher les résultats dans la console

---

## 🔧 Méthode 2 : Exécution Manuelle

### Étape 1 : Ouvrir PowerShell
```powershell
cd c:\Users\LENO\Desktop\Etragsarlu
```

### Étape 2 : Exécuter le script de test
```powershell
python manage.py shell < create_test_data.py
```

---

## 📊 Ce Qui Est Testé

### Test 1 : Validation d'une Dépense
- ✅ Création d'une dépense avec statut "En attente"
- ✅ Validation de la dépense (changement vers "Validée")
- ✅ Vérification de la création automatique d'une transaction
- ✅ Vérification de la déduction du montant du solde

**Montant testé** : 500,000 GNF

---

### Test 2 : Validation d'un Achat
- ✅ Création d'un achat avec statut "Brouillon"
- ✅ Ajout de lignes d'achat (produits)
- ✅ Validation de l'achat (changement vers "Validé")
- ✅ Vérification de la création automatique d'une transaction
- ✅ Vérification de la déduction du montant total

**Montant testé** : ~4,700,000 GNF (50 sacs ciment + 10 tonnes sable)

---

### Test 3 : Validation d'un Paiement Personnel
- ✅ Création d'un paiement avec statut "En attente"
- ✅ Validation du paiement (changement vers "Validé")
- ✅ Vérification de la création automatique d'une transaction
- ✅ Vérification de la déduction du montant

**Montant testé** : 750,000 GNF

---

## 📦 Données Créées

Le script crée automatiquement :

### 1. Utilisateur
- **Username** : admin
- **Password** : admin123
- **Email** : admin@etragsarlu.com

### 2. Client
- **Nom** : DIALLO Mamadou
- **Téléphone** : +224 622 123 456
- **Ville** : Conakry

### 3. Projet de Test
- **Code** : PROJ-TEST-001
- **Nom** : Villa Moderne Test
- **Budget initial** : 100,000,000 GNF
- **Dépôt initial** : 50,000,000 GNF
- **Solde de départ** : 150,000,000 GNF

### 4. Catégories de Dépenses
- Matériaux
- Main d'œuvre
- Transport
- Location

### 5. Fournisseurs
- Cimenterie de Guinée
- Société Métallique
- Transport Express

### 6. Produits
- Ciment Portland (85,000 GNF/sac)
- Sable (45,000 GNF/tonne)
- Gravier (55,000 GNF/tonne)
- Fer Ø12 (15,000 GNF/barre)

### 7. Personnel
- Mamadou DIALLO (Chef de chantier - 150,000 GNF/jour)
- Ibrahima CAMARA (Maçon - 80,000 GNF/jour)
- Amadou SOW (Ferrailleur - 70,000 GNF/jour)

---

## 📈 Résultats Attendus

### Solde Initial
```
Budget : 100,000,000 GNF
Dépôt  : +50,000,000 GNF
─────────────────────────
Solde  : 150,000,000 GNF
```

### Après Test 1 (Dépense)
```
Solde avant : 150,000,000 GNF
Dépense     : -500,000 GNF
─────────────────────────
Solde après : 149,500,000 GNF ✓
```

### Après Test 2 (Achat)
```
Solde avant : 149,500,000 GNF
Achat       : -4,700,000 GNF
─────────────────────────
Solde après : 144,800,000 GNF ✓
```

### Après Test 3 (Paiement)
```
Solde avant : 144,800,000 GNF
Paiement    : -750,000 GNF
─────────────────────────
Solde après : 144,050,000 GNF ✓
```

### Solde Final Attendu
```
150,000,000 - 500,000 - 4,700,000 - 750,000 = 144,050,000 GNF
```

---

## ✅ Vérification des Résultats

### Dans la Console
Le script affiche :
- ✅ ou ❌ pour chaque test
- Le solde avant et après chaque opération
- Les détails des transactions créées
- Un résumé final

### Dans l'Interface Web

1. **Accédez au dashboard** :
   ```
   http://127.0.0.1:8000/dashboard/
   ```

2. **Consultez le projet** :
   - Allez dans Projets → PROJ-TEST-001
   - Vérifiez le solde disponible

3. **Consultez les transactions** :
   - Allez dans Finances → Transactions
   - Filtrez par projet "PROJ-TEST-001"
   - Vous devriez voir :
     - 1 Dépôt de 50,000,000 GNF
     - 3 Dépenses automatiques (500,000 + 4,700,000 + 750,000)

4. **Consultez les opérations** :
   - **Dépenses** : Finances → Dépenses
   - **Achats** : Inventaire → Achats
   - **Paiements** : Personnel → Paiements

---

## 🔍 Interprétation des Résultats

### ✅ Test Réussi
```
✅ TEST X RÉUSSI : Déduction correcte !
```
- La transaction a été créée automatiquement
- Le montant a été correctement déduit du solde
- Le système fonctionne comme prévu

### ❌ Test Échoué
```
❌ TEST X ÉCHOUÉ : Déduction incorrecte !
```
- Vérifiez que les migrations sont appliquées
- Vérifiez que le serveur a été redémarré
- Consultez les logs d'erreur

---

## 🧹 Nettoyage des Données de Test

### Option 1 : Supprimer le projet de test
```python
python manage.py shell
>>> from apps.projects.models import Projet
>>> projet = Projet.objects.get(code_projet='PROJ-TEST-001')
>>> projet.delete()
>>> exit()
```

### Option 2 : Réinitialiser la base de données (⚠️ Attention)
```powershell
# Sauvegardez d'abord votre base de données !
python manage.py flush
```

---

## 🐛 Dépannage

### Erreur : "No module named 'apps'"
**Solution** : Assurez-vous d'être dans le bon répertoire
```powershell
cd c:\Users\LENO\Desktop\Etragsarlu
```

### Erreur : "DJANGO_SETTINGS_MODULE is not set"
**Solution** : Le script configure automatiquement Django, mais si l'erreur persiste :
```powershell
$env:DJANGO_SETTINGS_MODULE="config.settings"
python manage.py shell < create_test_data.py
```

### Erreur : "Table doesn't exist"
**Solution** : Appliquez les migrations
```powershell
python manage.py migrate
```

### Les tests échouent
**Solutions** :
1. Vérifiez que le serveur a été redémarré après les modifications
2. Vérifiez que les migrations sont appliquées
3. Consultez les logs Django pour plus de détails

---

## 📞 Support

Si les tests échouent de manière persistante :
1. Capturez la sortie complète de la console
2. Vérifiez les fichiers de log Django
3. Consultez la documentation technique (CHANGELOG_DEDUCTION.md)

---

## 🎯 Prochaines Étapes

Après avoir vérifié que les tests passent :
1. ✅ Testez manuellement dans l'interface web
2. ✅ Créez vos propres projets réels
3. ✅ Formez les utilisateurs avec le GUIDE_RAPIDE_DEDUCTION.txt
4. ✅ Consultez les exemples dans EXEMPLES_DEDUCTION.md

---

**Bonne chance avec vos tests !** 🚀
