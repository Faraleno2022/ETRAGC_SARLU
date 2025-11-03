from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from apps.finances.models import Transaction, Depense, CategorieDepense, Fournisseur
from apps.projects.models import Projet
from apps.clients.models import Client

User = get_user_model()


class TransactionModelTest(TestCase):
    """Tests pour le modèle Transaction"""
    
    def setUp(self):
        """Préparation des données de test"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.client = Client.objects.create(
            nom_complet='Client Test',
            telephone='622000000'
        )
        
        self.projet = Projet.objects.create(
            code_projet='PROJ-TEST-001',
            nom_projet='Projet Test',
            client=self.client,
            montant_prevu=Decimal('10000000.00'),
            date_debut=date.today(),
            statut='En_cours'
        )
    
    def test_depot_augmente_solde(self):
        """Test : Un dépôt augmente le solde disponible"""
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        self.assertEqual(self.projet.get_total_depots(), Decimal('5000000.00'))
        self.assertEqual(self.projet.get_solde_disponible(), Decimal('5000000.00'))
    
    def test_retrait_deduit_du_solde(self):
        """Test : Un retrait déduit du solde disponible"""
        # Créer un dépôt
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Créer un retrait
        Transaction.objects.create(
            projet=self.projet,
            type='Retrait',
            montant=Decimal('2000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        self.assertEqual(self.projet.get_total_retraits(), Decimal('2000000.00'))
        self.assertEqual(self.projet.get_solde_disponible(), Decimal('3000000.00'))
    
    def test_depense_deduit_du_budget(self):
        """Test : Une dépense déduit du budget disponible"""
        # Créer un dépôt
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Créer une dépense
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('1500000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        self.assertEqual(self.projet.get_total_depenses(), Decimal('1500000.00'))
        # Budget disponible = montant_prevu + dépôts - dépenses
        expected_budget = Decimal('10000000.00') + Decimal('5000000.00') - Decimal('1500000.00')
        self.assertEqual(self.projet.get_budget_disponible(), expected_budget)
    
    def test_calcul_budget_complet(self):
        """Test : Calcul complet avec dépôts, retraits et dépenses"""
        # Dépôt
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('8000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Retrait
        Transaction.objects.create(
            projet=self.projet,
            type='Retrait',
            montant=Decimal('3000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Dépense
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('2000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Vérifications
        self.assertEqual(self.projet.get_total_depots(), Decimal('8000000.00'))
        self.assertEqual(self.projet.get_total_retraits(), Decimal('3000000.00'))
        self.assertEqual(self.projet.get_total_depenses(), Decimal('2000000.00'))
        
        # Solde = Dépôts - Retraits
        self.assertEqual(self.projet.get_solde_disponible(), Decimal('5000000.00'))
        
        # Budget = Budget Prévu + Dépôts - Dépenses
        expected_budget = Decimal('10000000.00') + Decimal('8000000.00') - Decimal('2000000.00')
        self.assertEqual(self.projet.get_budget_disponible(), expected_budget)


class DepenseModelTest(TestCase):
    """Tests pour le modèle Depense"""
    
    def setUp(self):
        """Préparation des données de test"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.client = Client.objects.create(
            nom_complet='Client Test',
            telephone='622000000'
        )
        
        self.projet = Projet.objects.create(
            code_projet='PROJ-TEST-002',
            nom_projet='Projet Test 2',
            client=self.client,
            montant_prevu=Decimal('5000000.00'),
            date_debut=date.today(),
            statut='En_cours'
        )
        
        self.categorie = CategorieDepense.objects.create(
            nom='Transport',
            code='TRANS'
        )
        
        self.fournisseur = Fournisseur.objects.create(
            nom='Fournisseur Test',
            type='Services'
        )
    
    def test_validation_depense_cree_transaction(self):
        """Test : La validation d'une dépense crée une transaction"""
        depense = Depense.objects.create(
            projet=self.projet,
            categorie=self.categorie,
            fournisseur=self.fournisseur,
            date_depense=date.today(),
            montant=Decimal('500000.00'),
            mode_paiement='Espèces',
            statut='En_attente',
            saisi_par=self.user
        )
        
        # Vérifier qu'aucune transaction n'existe avant validation
        transactions_count_before = Transaction.objects.filter(projet=self.projet).count()
        self.assertEqual(transactions_count_before, 0)
        
        # Valider la dépense
        depense.statut = 'Validée'
        depense.save()
        
        # Vérifier qu'une transaction a été créée
        transactions_count_after = Transaction.objects.filter(projet=self.projet).count()
        self.assertEqual(transactions_count_after, 1)
        
        # Vérifier les détails de la transaction
        transaction = Transaction.objects.get(projet=self.projet)
        self.assertEqual(transaction.type, 'Dépense')
        self.assertEqual(transaction.montant, Decimal('500000.00'))
        self.assertEqual(transaction.statut, 'Validée')
