from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from apps.projects.models import Projet
from apps.clients.models import Client
from apps.finances.models import Transaction

User = get_user_model()


class ProjetBudgetTest(TestCase):
    """Tests pour les calculs de budget du projet"""
    
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
            nom_projet='Projet Test Budget',
            client=self.client,
            montant_prevu=Decimal('10000000.00'),
            date_debut=date.today(),
            statut='En_cours'
        )
    
    def test_budget_initial(self):
        """Test : Budget initial sans transactions"""
        self.assertEqual(self.projet.get_total_depots(), Decimal('0'))
        self.assertEqual(self.projet.get_total_retraits(), Decimal('0'))
        self.assertEqual(self.projet.get_total_depenses(), Decimal('0'))
        self.assertEqual(self.projet.get_solde_disponible(), Decimal('0'))
        self.assertEqual(self.projet.get_budget_disponible(), Decimal('10000000.00'))
    
    def test_formule_solde_disponible(self):
        """Test : Solde Disponible = Dépôts - Retraits"""
        # Créer des dépôts
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('8000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('2000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Créer des retraits
        Transaction.objects.create(
            projet=self.projet,
            type='Retrait',
            montant=Decimal('3000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        Transaction.objects.create(
            projet=self.projet,
            type='Retrait',
            montant=Decimal('1000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Vérifier la formule : Solde = Dépôts - Retraits
        total_depots = Decimal('10000000.00')
        total_retraits = Decimal('4000000.00')
        solde_attendu = total_depots - total_retraits
        
        self.assertEqual(self.projet.get_total_depots(), total_depots)
        self.assertEqual(self.projet.get_total_retraits(), total_retraits)
        self.assertEqual(self.projet.get_solde_disponible(), solde_attendu)
    
    def test_formule_budget_disponible(self):
        """Test : Budget Disponible = Budget Prévu + Dépôts - Dépenses"""
        # Créer un dépôt
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Créer des dépenses
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('2000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Paiement Personnel',
            montant=Decimal('1500000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Vérifier la formule : Budget = Budget Prévu + Dépôts - Dépenses
        budget_prevu = Decimal('10000000.00')
        total_depots = Decimal('5000000.00')
        total_depenses = Decimal('3500000.00')
        budget_attendu = budget_prevu + total_depots - total_depenses
        
        self.assertEqual(self.projet.get_total_depots(), total_depots)
        self.assertEqual(self.projet.get_total_depenses(), total_depenses)
        self.assertEqual(self.projet.get_budget_disponible(), budget_attendu)
    
    def test_retraits_non_inclus_dans_depenses(self):
        """Test : Les retraits ne sont PAS inclus dans les dépenses"""
        # Créer un retrait
        Transaction.objects.create(
            projet=self.projet,
            type='Retrait',
            montant=Decimal('2000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Créer une dépense
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('1000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Vérifier que les retraits ne sont pas dans les dépenses
        self.assertEqual(self.projet.get_total_retraits(), Decimal('2000000.00'))
        self.assertEqual(self.projet.get_total_depenses(), Decimal('1000000.00'))
        
        # Les retraits affectent le solde, pas le budget
        self.assertEqual(self.projet.get_solde_disponible(), Decimal('-2000000.00'))
        self.assertEqual(self.projet.get_budget_disponible(), Decimal('9000000.00'))
    
    def test_scenario_complet(self):
        """Test : Scénario complet avec tous les types de transactions"""
        # Budget initial : 10,000,000
        
        # Dépôt client : 8,000,000
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('8000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Retrait pour caisse : 3,000,000
        Transaction.objects.create(
            projet=self.projet,
            type='Retrait',
            montant=Decimal('3000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Achat matériaux : 2,500,000
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('2500000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Paiement personnel : 1,200,000
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Paiement Personnel',
            montant=Decimal('1200000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Autre dépense : 800,000
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Transport',
            montant=Decimal('800000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Vérifications
        self.assertEqual(self.projet.get_total_depots(), Decimal('8000000.00'))
        self.assertEqual(self.projet.get_total_retraits(), Decimal('3000000.00'))
        self.assertEqual(self.projet.get_total_depenses(), Decimal('4500000.00'))
        
        # Solde = Dépôts - Retraits = 8,000,000 - 3,000,000 = 5,000,000
        self.assertEqual(self.projet.get_solde_disponible(), Decimal('5000000.00'))
        
        # Budget = Budget Prévu + Dépôts - Dépenses
        # Budget = 10,000,000 + 8,000,000 - 4,500,000 = 13,500,000
        self.assertEqual(self.projet.get_budget_disponible(), Decimal('13500000.00'))
    
    def test_transactions_non_validees_non_comptees(self):
        """Test : Les transactions non validées ne sont pas comptées"""
        # Créer des transactions en attente
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='En_attente',
            saisi_par=self.user
        )
        
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('1000000.00'),
            date_transaction=date.today(),
            statut='En_attente',
            saisi_par=self.user
        )
        
        # Vérifier qu'elles ne sont pas comptées
        self.assertEqual(self.projet.get_total_depots(), Decimal('0'))
        self.assertEqual(self.projet.get_total_depenses(), Decimal('0'))
        self.assertEqual(self.projet.get_budget_disponible(), Decimal('10000000.00'))
    
    def test_pourcentage_budget_consomme(self):
        """Test : Calcul du pourcentage de budget consommé"""
        # Dépôt
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('10000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Dépense de 25% du budget total
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Budget total = 10,000,000 + 10,000,000 = 20,000,000
        # Dépenses = 5,000,000
        # Pourcentage = 25%
        pourcentage = self.projet.get_pourcentage_budget_consomme()
        self.assertEqual(pourcentage, 25.0)
    
    def test_budget_depasse(self):
        """Test : Détection de dépassement de budget"""
        # Créer des dépenses supérieures au budget
        Transaction.objects.create(
            projet=self.projet,
            type='Dépense',
            categorie='Achat Matériaux',
            montant=Decimal('12000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        # Vérifier que le budget est dépassé
        self.assertTrue(self.projet.is_budget_depasse())
        self.assertLess(self.projet.get_budget_disponible(), 0)
