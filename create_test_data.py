"""
Script de création de données de test pour vérifier le système de déduction automatique
Exécuter avec : python manage.py shell < create_test_data.py
"""

import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.clients.models import Client
from apps.projects.models import Projet
from apps.finances.models import Transaction, CategorieDepense, Fournisseur, Depense
from apps.inventory.models import (
    UniteMessure, CategorieProduit, Produit, Stock, Achat, LigneAchat
)
from apps.personnel.models import Personnel, AffectationPersonnel, PaiementPersonnel

User = get_user_model()

print("=" * 70)
print("CRÉATION DES DONNÉES DE TEST - SYSTÈME DE DÉDUCTION AUTOMATIQUE")
print("=" * 70)

# ============================================================================
# 1. CRÉATION DE L'UTILISATEUR ADMIN
# ============================================================================
print("\n[1/10] Création de l'utilisateur admin...")
try:
    admin_user = User.objects.get(username='admin')
    print(f"✓ Utilisateur 'admin' existe déjà (ID: {admin_user.id})")
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@etragsarlu.com',
        password='admin123',
        first_name='Administrateur',
        last_name='Système'
    )
    print(f"✓ Utilisateur 'admin' créé (ID: {admin_user.id})")

# ============================================================================
# 2. CRÉATION DU CLIENT
# ============================================================================
print("\n[2/10] Création du client...")
client, created = Client.objects.get_or_create(
    nom='DIALLO',
    prenom='Mamadou',
    defaults={
        'telephone': '+224 622 123 456',
        'email': 'mamadou.diallo@example.com',
        'adresse': 'Quartier Kaloum, Conakry',
        'ville': 'Conakry',
        'type_client': 'Particulier',
    }
)
if created:
    print(f"✓ Client créé : {client.get_full_name()} (ID: {client.id})")
else:
    print(f"✓ Client existe : {client.get_full_name()} (ID: {client.id})")

# ============================================================================
# 3. CRÉATION DU PROJET
# ============================================================================
print("\n[3/10] Création du projet de test...")
projet, created = Projet.objects.get_or_create(
    code_projet='PROJ-TEST-001',
    defaults={
        'nom_projet': 'Villa Moderne Test',
        'client': client,
        'type_projet': 'Construction',
        'adresse_chantier': 'Kaloum, Conakry',
        'ville': 'Conakry',
        'montant_prevu': Decimal('100000000.00'),  # 100 millions GNF
        'date_debut': date.today() - timedelta(days=10),
        'date_fin_prevue': date.today() + timedelta(days=80),
        'statut': 'En_cours',
        'description': 'Projet de test pour vérifier la déduction automatique',
    }
)
if created:
    print(f"✓ Projet créé : {projet.code_projet} - {projet.nom_projet}")
    print(f"  Budget initial : {projet.montant_prevu:,.0f} GNF")
else:
    print(f"✓ Projet existe : {projet.code_projet} - {projet.nom_projet}")

# ============================================================================
# 4. CRÉATION D'UN DÉPÔT INITIAL
# ============================================================================
print("\n[4/10] Création d'un dépôt initial...")
depot, created = Transaction.objects.get_or_create(
    projet=projet,
    type='Dépôt',
    date_transaction=date.today() - timedelta(days=9),
    defaults={
        'montant': Decimal('50000000.00'),  # 50 millions GNF
        'reference': 'DEP-TEST-001',
        'mode_paiement': 'Virement',
        'statut': 'Validée',
        'description': 'Dépôt initial client - Test',
        'saisi_par': admin_user,
    }
)
if created:
    print(f"✓ Dépôt créé : {depot.montant:,.0f} GNF")
    print(f"  Solde actuel : {projet.get_budget_disponible():,.0f} GNF")
else:
    print(f"✓ Dépôt existe : {depot.montant:,.0f} GNF")

# ============================================================================
# 5. CRÉATION DES CATÉGORIES DE DÉPENSES
# ============================================================================
print("\n[5/10] Création des catégories de dépenses...")
categories_data = [
    ('Matériaux', 'MAT', '#3B82F6'),
    ('Main d\'œuvre', 'MO', '#10B981'),
    ('Transport', 'TRA', '#F59E0B'),
    ('Location', 'LOC', '#8B5CF6'),
]

categories = {}
for nom, code, couleur in categories_data:
    cat, created = CategorieDepense.objects.get_or_create(
        nom=nom,
        defaults={'code': code, 'couleur_hex': couleur}
    )
    categories[nom] = cat
    status = "créée" if created else "existe"
    print(f"  • {nom} : {status}")

# ============================================================================
# 6. CRÉATION DES FOURNISSEURS
# ============================================================================
print("\n[6/10] Création des fournisseurs...")
fournisseurs_data = [
    ('Cimenterie de Guinée', 'Matériaux', '+224 622 111 111'),
    ('Société Métallique', 'Matériaux', '+224 622 222 222'),
    ('Transport Express', 'Transport', '+224 622 333 333'),
]

fournisseurs = {}
for nom, type_f, tel in fournisseurs_data:
    fourn, created = Fournisseur.objects.get_or_create(
        nom=nom,
        defaults={
            'type': type_f,
            'telephone': tel,
            'ville': 'Conakry',
        }
    )
    fournisseurs[nom] = fourn
    status = "créé" if created else "existe"
    print(f"  • {nom} : {status}")

# ============================================================================
# 7. CRÉATION DES UNITÉS ET PRODUITS
# ============================================================================
print("\n[7/10] Création des unités et produits...")

# Unités de mesure
unite_sac, _ = UniteMessure.objects.get_or_create(
    nom='Sac', defaults={'symbole': 'sac'}
)
unite_tonne, _ = UniteMessure.objects.get_or_create(
    nom='Tonne', defaults={'symbole': 't'}
)
unite_barre, _ = UniteMessure.objects.get_or_create(
    nom='Barre', defaults={'symbole': 'barre'}
)

# Catégories de produits
cat_ciment, _ = CategorieProduit.objects.get_or_create(
    nom='Ciment', defaults={'code': 'CIM'}
)
cat_agregat, _ = CategorieProduit.objects.get_or_create(
    nom='Agrégats', defaults={'code': 'AGR'}
)
cat_fer, _ = CategorieProduit.objects.get_or_create(
    nom='Ferraillage', defaults={'code': 'FER'}
)

# Produits
produits_data = [
    ('Ciment Portland', cat_ciment, unite_sac, 85000),
    ('Sable', cat_agregat, unite_tonne, 45000),
    ('Gravier', cat_agregat, unite_tonne, 55000),
    ('Fer Ø12', cat_fer, unite_barre, 15000),
]

produits = {}
for nom, cat, unite, prix in produits_data:
    # Chercher ou créer le produit
    prod = Produit.objects.filter(nom=nom).first()
    if not prod:
        prod = Produit.objects.create(
            nom=nom,
            categorie=cat,
            unite_mesure=unite,
            prix_unitaire_moyen=Decimal(str(prix)),
            stock_minimum=Decimal('10.00'),
        )
        print(f"  • Produit créé : {nom}")
    else:
        print(f"  • Produit existe : {nom}")
    produits[nom] = prod
    
    # Créer le stock pour le projet
    stock, created = Stock.objects.get_or_create(
        projet=projet,
        produit=prod,
        defaults={'quantite_actuelle': Decimal('0.00')}
    )

# ============================================================================
# 8. CRÉATION DU PERSONNEL
# ============================================================================
print("\n[8/10] Création du personnel...")
personnel_data = [
    ('DIALLO', 'Mamadou', 'Chef_Chantier', 'CDI', 150000),
    ('CAMARA', 'Ibrahima', 'Maçon', 'Journalier', 80000),
    ('SOW', 'Amadou', 'Ferrailleur', 'Journalier', 70000),
]

personnels = {}
for nom, prenom, fonction, contrat, salaire in personnel_data:
    pers, created = Personnel.objects.get_or_create(
        nom=nom,
        prenom=prenom,
        defaults={
            'fonction': fonction,
            'type_contrat': contrat,
            'salaire_journalier': Decimal(str(salaire)),
            'telephone': f'+224 622 {hash(nom) % 900000 + 100000}',
            'date_embauche': date.today() - timedelta(days=30),
        }
    )
    personnels[f"{prenom} {nom}"] = pers
    status = "créé" if created else "existe"
    print(f"  • {prenom} {nom} ({fonction}) : {status}")
    
    # Affecter au projet
    affectation, aff_created = AffectationPersonnel.objects.get_or_create(
        personnel=pers,
        projet=projet,
        date_debut=date.today() - timedelta(days=8),
        defaults={
            'role_chantier': 'Chef' if fonction == 'Chef_Chantier' else 'Ouvrier',
        }
    )

print(f"\n✓ Solde avant tests : {projet.get_budget_disponible():,.0f} GNF")

# ============================================================================
# 9. TEST 1 : CRÉATION ET VALIDATION D'UNE DÉPENSE
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1 : VALIDATION D'UNE DÉPENSE")
print("=" * 70)

solde_avant = projet.get_budget_disponible()
print(f"Solde avant : {solde_avant:,.0f} GNF")

# Créer une dépense en attente
depense_test = Depense.objects.create(
    projet=projet,
    categorie=categories['Transport'],
    fournisseur=fournisseurs['Transport Express'],
    date_depense=date.today() - timedelta(days=5),
    montant=Decimal('500000.00'),  # 500,000 GNF
    mode_paiement='Espèces',
    description='Location camion - Test déduction',
    saisi_par=admin_user,
    statut='En_attente',
)
print(f"\n✓ Dépense créée (ID: {depense_test.id}) - Statut: En_attente")
print(f"  Montant : {depense_test.montant:,.0f} GNF")

# Compter les transactions avant validation
nb_transactions_avant = Transaction.objects.filter(projet=projet).count()
print(f"  Transactions avant validation : {nb_transactions_avant}")

# VALIDER LA DÉPENSE (déclenchement automatique)
print("\n→ Validation de la dépense...")
depense_test.statut = 'Validée'
depense_test.save()

# Vérifier la création de la transaction
nb_transactions_apres = Transaction.objects.filter(projet=projet).count()
print(f"  Transactions après validation : {nb_transactions_apres}")

if nb_transactions_apres > nb_transactions_avant:
    transaction_creee = Transaction.objects.filter(
        projet=projet,
        type='Dépense',
        categorie='Transport'
    ).latest('date_creation')
    print(f"\n✅ Transaction automatique créée !")
    print(f"  ID: {transaction_creee.id}")
    print(f"  Type: {transaction_creee.type}")
    print(f"  Catégorie: {transaction_creee.categorie}")
    print(f"  Montant: {transaction_creee.montant:,.0f} GNF")
    print(f"  Statut: {transaction_creee.statut}")
else:
    print("\n❌ ERREUR : Aucune transaction créée !")

solde_apres = projet.get_budget_disponible()
print(f"\nSolde après : {solde_apres:,.0f} GNF")
print(f"Différence : {solde_avant - solde_apres:,.0f} GNF")

if solde_avant - solde_apres == depense_test.montant:
    print("✅ TEST 1 RÉUSSI : Déduction correcte !")
else:
    print("❌ TEST 1 ÉCHOUÉ : Déduction incorrecte !")

# ============================================================================
# 10. TEST 2 : CRÉATION ET VALIDATION D'UN ACHAT
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2 : VALIDATION D'UN ACHAT")
print("=" * 70)

solde_avant = projet.get_budget_disponible()
print(f"Solde avant : {solde_avant:,.0f} GNF")

# Créer un achat en brouillon
achat_test = Achat.objects.create(
    projet=projet,
    fournisseur=fournisseurs['Cimenterie de Guinée'],
    date_achat=date.today() - timedelta(days=3),
    mode_paiement='Espèces',
    saisi_par=admin_user,
    statut='Brouillon',
)
print(f"\n✓ Achat créé (ID: {achat_test.id}) - Statut: Brouillon")
print(f"  N°: {achat_test.numero_achat}")

# Ajouter des lignes d'achat
ligne1 = LigneAchat.objects.create(
    achat=achat_test,
    produit=produits['Ciment Portland'],
    quantite=Decimal('50.00'),
    prix_unitaire=Decimal('85000.00'),
)
ligne2 = LigneAchat.objects.create(
    achat=achat_test,
    produit=produits['Sable'],
    quantite=Decimal('10.00'),
    prix_unitaire=Decimal('45000.00'),
)

achat_test.refresh_from_db()
print(f"  Montant total : {achat_test.montant_total:,.0f} GNF")

# Compter les transactions avant validation
nb_transactions_avant = Transaction.objects.filter(projet=projet).count()
print(f"  Transactions avant validation : {nb_transactions_avant}")

# VALIDER L'ACHAT (déclenchement automatique)
print("\n→ Validation de l'achat...")
achat_test.statut = 'Validé'
achat_test.save()

# Vérifier la création de la transaction
nb_transactions_apres = Transaction.objects.filter(projet=projet).count()
print(f"  Transactions après validation : {nb_transactions_apres}")

if nb_transactions_apres > nb_transactions_avant:
    transaction_creee = Transaction.objects.filter(
        projet=projet,
        type='Dépense',
        categorie='Achat Matériaux'
    ).latest('date_creation')
    print(f"\n✅ Transaction automatique créée !")
    print(f"  ID: {transaction_creee.id}")
    print(f"  Type: {transaction_creee.type}")
    print(f"  Catégorie: {transaction_creee.categorie}")
    print(f"  Montant: {transaction_creee.montant:,.0f} GNF")
    print(f"  Statut: {transaction_creee.statut}")
else:
    print("\n❌ ERREUR : Aucune transaction créée !")

solde_apres = projet.get_budget_disponible()
print(f"\nSolde après : {solde_apres:,.0f} GNF")
print(f"Différence : {solde_avant - solde_apres:,.0f} GNF")

if solde_avant - solde_apres == achat_test.montant_total:
    print("✅ TEST 2 RÉUSSI : Déduction correcte !")
else:
    print("❌ TEST 2 ÉCHOUÉ : Déduction incorrecte !")

# ============================================================================
# 11. TEST 3 : CRÉATION ET VALIDATION D'UN PAIEMENT PERSONNEL
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3 : VALIDATION D'UN PAIEMENT PERSONNEL")
print("=" * 70)

solde_avant = projet.get_budget_disponible()
print(f"Solde avant : {solde_avant:,.0f} GNF")

# Créer un paiement en attente
chef = personnels['Mamadou DIALLO']
paiement_test = PaiementPersonnel.objects.create(
    personnel=chef,
    projet=projet,
    date_paiement=date.today() - timedelta(days=2),
    montant=Decimal('750000.00'),  # 750,000 GNF
    nombre_jours=5,
    mode_paiement='Mobile_Money',
    description='Avance salaire - Test déduction',
    saisi_par=admin_user,
    statut='En_attente',
)
print(f"\n✓ Paiement créé (ID: {paiement_test.id}) - Statut: En_attente")
print(f"  Personnel : {chef.get_full_name()}")
print(f"  Montant : {paiement_test.montant:,.0f} GNF")

# Compter les transactions avant validation
nb_transactions_avant = Transaction.objects.filter(projet=projet).count()
print(f"  Transactions avant validation : {nb_transactions_avant}")

# VALIDER LE PAIEMENT (déclenchement automatique)
print("\n→ Validation du paiement...")
paiement_test.statut = 'Validé'
paiement_test.save()

# Vérifier la création de la transaction
nb_transactions_apres = Transaction.objects.filter(projet=projet).count()
print(f"  Transactions après validation : {nb_transactions_apres}")

if nb_transactions_apres > nb_transactions_avant:
    transaction_creee = Transaction.objects.filter(
        projet=projet,
        type='Dépense',
        categorie='Paiement Personnel'
    ).latest('date_creation')
    print(f"\n✅ Transaction automatique créée !")
    print(f"  ID: {transaction_creee.id}")
    print(f"  Type: {transaction_creee.type}")
    print(f"  Catégorie: {transaction_creee.categorie}")
    print(f"  Montant: {transaction_creee.montant:,.0f} GNF")
    print(f"  Statut: {transaction_creee.statut}")
else:
    print("\n❌ ERREUR : Aucune transaction créée !")

solde_apres = projet.get_budget_disponible()
print(f"\nSolde après : {solde_apres:,.0f} GNF")
print(f"Différence : {solde_avant - solde_apres:,.0f} GNF")

if solde_avant - solde_apres == paiement_test.montant:
    print("✅ TEST 3 RÉUSSI : Déduction correcte !")
else:
    print("❌ TEST 3 ÉCHOUÉ : Déduction incorrecte !")

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================
print("\n" + "=" * 70)
print("RÉSUMÉ FINAL")
print("=" * 70)

print(f"\nProjet : {projet.code_projet} - {projet.nom_projet}")
print(f"Budget initial : {projet.montant_prevu:,.0f} GNF")
print(f"Total dépôts : {projet.get_total_depots():,.0f} GNF")
print(f"Total dépenses : {projet.get_total_depenses():,.0f} GNF")
print(f"Solde disponible : {projet.get_budget_disponible():,.0f} GNF")

print(f"\nNombre total de transactions : {Transaction.objects.filter(projet=projet).count()}")
print(f"  - Dépôts : {Transaction.objects.filter(projet=projet, type='Dépôt').count()}")
print(f"  - Dépenses : {Transaction.objects.filter(projet=projet, type='Dépense').count()}")

print("\n" + "=" * 70)
print("TESTS TERMINÉS !")
print("=" * 70)
print("\nConsultez le dashboard pour voir les résultats dans l'interface.")
print("URL : http://127.0.0.1:8000/dashboard/")
