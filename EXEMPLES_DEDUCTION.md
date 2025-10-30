# 📖 Exemples Pratiques - Déduction Automatique

## 🏗️ Scénario Complet : Construction d'une Villa

### Situation Initiale
```
Projet : Villa Moderne à Kaloum
Code : PROJ-2025-001
Budget initial : 150,000,000 GNF
Statut : En cours
```

---

## 📅 Semaine 1 : Démarrage du Projet

### Jour 1 : Réception du premier dépôt client
**Action** : Finances → Transactions → Nouveau Dépôt
```
Type : Dépôt
Montant : 50,000,000 GNF
Date : 20/10/2025
Mode : Virement
Statut : Validée
```

**Résultat** :
```
Solde = 150,000,000 + 50,000,000 = 200,000,000 GNF ✓
```

---

### Jour 2 : Achat de matériaux de base
**Action** : Inventaire → Achats → Nouvel Achat
```
Fournisseur : Cimenterie de Guinée
Date : 21/10/2025
Mode paiement : Espèces

Lignes d'achat :
- 100 sacs de ciment @ 85,000 = 8,500,000 GNF
- 50 tonnes de sable @ 45,000 = 2,250,000 GNF
- 30 tonnes de gravier @ 55,000 = 1,650,000 GNF

Montant total : 12,400,000 GNF
Statut : Brouillon → Validé
```

**Ce qui se passe automatiquement** :
```
✓ Transaction créée :
  - Type : Dépense
  - Catégorie : Achat Matériaux
  - Montant : 12,400,000 GNF
  - Description : Achat ACH-2025-0001 - Cimenterie de Guinée

✓ Nouveau solde = 200,000,000 - 12,400,000 = 187,600,000 GNF
```

---

### Jour 3 : Embauche et affectation du personnel
**Action** : Personnel → Affectations
```
Personnel affectés :
- Chef de chantier : Mamadou Diallo
- 5 Maçons
- 3 Ferrailleurs
- 2 Manœuvres
```
*(Pas de déduction à ce stade - juste l'affectation)*

---

### Jour 5 : Premier paiement du personnel
**Action** : Personnel → Paiements → Nouveau Paiement
```
Personnel : Mamadou Diallo (Chef de chantier)
Projet : PROJ-2025-001
Date : 25/10/2025
Montant : 1,500,000 GNF
Nombre de jours : 5
Mode paiement : Mobile Money
Description : Avance sur salaire
Statut : En attente → Validé
```

**Ce qui se passe automatiquement** :
```
✓ Transaction créée :
  - Type : Dépense
  - Catégorie : Paiement Personnel
  - Montant : 1,500,000 GNF
  - Description : Paiement Mamadou Diallo - Avance sur salaire

✓ Nouveau solde = 187,600,000 - 1,500,000 = 186,100,000 GNF
```

---

## 📅 Semaine 2 : Intensification des Travaux

### Jour 8 : Dépense pour location d'engins
**Action** : Finances → Dépenses → Nouvelle Dépense
```
Catégorie : Transport
Fournisseur : Location Engins Conakry
Date : 28/10/2025
Montant : 3,500,000 GNF
Mode paiement : Chèque
Description : Location pelleteuse - 7 jours
Statut : En attente → Validée
```

**Ce qui se passe automatiquement** :
```
✓ Transaction créée :
  - Type : Dépense
  - Catégorie : Transport
  - Montant : 3,500,000 GNF
  - Description : Dépense Transport - Location pelleteuse - 7 jours

✓ Nouveau solde = 186,100,000 - 3,500,000 = 182,600,000 GNF
```

---

### Jour 10 : Achat de ferraillage
**Action** : Inventaire → Achats → Nouvel Achat
```
Fournisseur : Société Métallique de Guinée
Date : 30/10/2025
Mode paiement : Virement

Lignes d'achat :
- 500 barres de fer Ø12 @ 15,000 = 7,500,000 GNF
- 300 barres de fer Ø10 @ 12,000 = 3,600,000 GNF
- 100 kg fil à ligaturer @ 8,000 = 800,000 GNF

Montant total : 11,900,000 GNF
Statut : Brouillon → Validé → Reçu
```

**Ce qui se passe automatiquement** :
```
✓ Transaction créée (lors du passage à "Validé") :
  - Type : Dépense
  - Catégorie : Achat Matériaux
  - Montant : 11,900,000 GNF
  - Description : Achat ACH-2025-0002 - Société Métallique de Guinée

✓ Stock mis à jour (lors du passage à "Reçu")

✓ Nouveau solde = 182,600,000 - 11,900,000 = 170,700,000 GNF
```

---

### Jour 12 : Paiement hebdomadaire des ouvriers
**Action** : Personnel → Paiements → Paiements multiples
```
5 Maçons @ 80,000/jour × 7 jours = 2,800,000 GNF
3 Ferrailleurs @ 70,000/jour × 7 jours = 1,470,000 GNF
2 Manœuvres @ 50,000/jour × 7 jours = 700,000 GNF

Total : 4,970,000 GNF
Mode paiement : Espèces
Statut : En attente → Validé
```

**Ce qui se passe automatiquement** :
```
✓ 10 Transactions créées (une par paiement) :
  - Type : Dépense
  - Catégorie : Paiement Personnel
  - Total : 4,970,000 GNF

✓ Nouveau solde = 170,700,000 - 4,970,000 = 165,730,000 GNF
```

---

## 📊 Résumé du Mois

### Tableau récapitulatif

| Date | Opération | Type | Montant | Solde |
|------|-----------|------|---------|-------|
| 20/10 | Dépôt client | Dépôt | +50,000,000 | 200,000,000 |
| 21/10 | Achat matériaux base | Achat | -12,400,000 | 187,600,000 |
| 25/10 | Paiement chef chantier | Paiement | -1,500,000 | 186,100,000 |
| 28/10 | Location engins | Dépense | -3,500,000 | 182,600,000 |
| 30/10 | Achat ferraillage | Achat | -11,900,000 | 170,700,000 |
| 01/11 | Paiements ouvriers | Paiement | -4,970,000 | 165,730,000 |

### Statistiques

```
Budget initial : 150,000,000 GNF
Total dépôts : 50,000,000 GNF
Total dépenses : 34,270,000 GNF

Répartition des dépenses :
- Achats matériaux : 24,300,000 GNF (71%)
- Paiements personnel : 6,470,000 GNF (19%)
- Autres dépenses : 3,500,000 GNF (10%)

Solde disponible : 165,730,000 GNF
Budget consommé : 17.1%
```

---

## 🎯 Cas Particuliers

### Cas 1 : Annulation puis re-validation
```
Achat créé → Validé → Transaction créée ✓
Achat annulé → Transaction reste (pas de suppression)
Achat re-validé → Nouvelle transaction créée ✓

⚠️ Attention : Deux transactions pour le même achat !
Solution : Supprimer manuellement la première transaction
```

### Cas 2 : Modification du montant après validation
```
Dépense validée → Transaction créée avec montant X ✓
Montant modifié → Transaction reste avec montant X
⚠️ Attention : Décalage entre dépense et transaction

Solution : 
1. Repasser en "En attente"
2. Supprimer la transaction créée
3. Modifier le montant
4. Re-valider
```

### Cas 3 : Achat en crédit
```
Mode paiement : Crédit
Transaction créée avec mode : Espèces (conversion automatique)
Raison : Le mode "Crédit" n'est pas un mode de paiement réel
```

---

## ✅ Bonnes Pratiques

### 1. Vérification avant validation
```
☑ Montant correct
☑ Date correcte
☑ Catégorie/Fournisseur correct
☑ Description claire
☑ Pièces justificatives attachées
→ Puis valider
```

### 2. Suivi régulier
```
• Consulter le solde du projet quotidiennement
• Vérifier les transactions créées automatiquement
• Rapprocher avec les pièces justificatives
• Générer des rapports hebdomadaires
```

### 3. Gestion des erreurs
```
Si erreur détectée :
1. NE PAS annuler l'opération validée
2. Créer une opération de correction
3. Documenter dans les notes
4. Informer le responsable
```

---

## 📈 Rapports Disponibles

### Rapport des transactions automatiques
```sql
-- Requête pour voir toutes les déductions automatiques
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

### Rapport du solde quotidien
```
Consultez : Projets → [Votre Projet] → Onglet "Finances"
Graphique : Évolution du solde dans le temps
```

---

**Pour plus d'informations, consultez** :
- `DEDUCTION_AUTOMATIQUE.md` - Documentation complète
- `GUIDE_RAPIDE_DEDUCTION.txt` - Guide rapide
- `CHANGELOG_DEDUCTION.md` - Détails techniques
