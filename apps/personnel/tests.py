from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from apps.personnel.models import Personnel, PaiementPersonnel, AffectationPersonnel
from apps.projects.models import Projet
from apps.clients.models import Client
from apps.finances.models import Transaction

User = get_user_model()


class PersonnelModelTest(TestCase):
    """Tests pour le modèle Personnel"""
    
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
        
        self.personnel = Personnel.objects.create(
            nom='Diallo',
            prenom='Mamadou',
            telephone='622111111',
            fonction='Maçon',
            type_contrat='Journalier',
            salaire_journalier=Decimal('50000.00'),
            salaire_convenu=Decimal('2000000.00'),
            actif=True
        )
    
    def test_salaire_convenu_existe(self):
        """Test : Le champ salaire_convenu existe et fonctionne"""
        self.assertEqual(self.personnel.salaire_convenu, Decimal('2000000.00'))
    
    def test_calcul_solde_salaire_convenu_sans_paiement(self):
        """Test : Solde = salaire_convenu quand aucun paiement"""
        solde = self.personnel.get_solde_salaire_convenu()
        self.assertEqual(solde, Decimal('2000000.00'))
    
    def test_calcul_solde_salaire_convenu_avec_paiement(self):
        """Test : Solde diminue après un paiement"""
        # Créer un paiement validé
        PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('500000.00'),
            mode_paiement='Espèces',
            statut='Validé',
            saisi_par=self.user
        )
        
        # Vérifier le solde
        solde = self.personnel.get_solde_salaire_convenu()
        self.assertEqual(solde, Decimal('1500000.00'))
    
    def test_calcul_solde_avec_plusieurs_paiements(self):
        """Test : Solde avec plusieurs paiements"""
        # Créer plusieurs paiements
        PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('500000.00'),
            mode_paiement='Espèces',
            statut='Validé',
            saisi_par=self.user
        )
        
        PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('300000.00'),
            mode_paiement='Espèces',
            statut='Validé',
            saisi_par=self.user
        )
        
        # Vérifier le solde
        solde = self.personnel.get_solde_salaire_convenu()
        self.assertEqual(solde, Decimal('1200000.00'))
    
    def test_pourcentage_paye(self):
        """Test : Calcul du pourcentage payé"""
        # Créer un paiement de 25% du salaire convenu
        PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('500000.00'),  # 25% de 2000000
            mode_paiement='Espèces',
            statut='Validé',
            saisi_par=self.user
        )
        
        # Vérifier le pourcentage
        pourcentage = self.personnel.get_pourcentage_paye()
        self.assertEqual(pourcentage, Decimal('25.00'))
    
    def test_paiement_en_attente_non_compte(self):
        """Test : Les paiements en attente ne sont pas comptés"""
        # Créer un paiement en attente
        PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('500000.00'),
            mode_paiement='Espèces',
            statut='En_attente',
            saisi_par=self.user
        )
        
        # Vérifier que le solde n'a pas changé
        solde = self.personnel.get_solde_salaire_convenu()
        self.assertEqual(solde, Decimal('2000000.00'))
    
    def test_personnel_sans_salaire_convenu(self):
        """Test : Personnel sans salaire convenu"""
        personnel2 = Personnel.objects.create(
            nom='Bah',
            prenom='Ibrahima',
            telephone='622222222',
            fonction='Électricien',
            type_contrat='CDD',
            salaire_journalier=Decimal('60000.00'),
            salaire_convenu=None,
            actif=True
        )
        
        # Vérifier que le solde est 0
        solde = personnel2.get_solde_salaire_convenu()
        self.assertEqual(solde, Decimal('0'))


class PaiementPersonnelModelTest(TestCase):
    """Tests pour le modèle PaiementPersonnel"""
    
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
            montant_prevu=Decimal('10000000.00'),
            date_debut=date.today(),
            statut='En_cours'
        )
        
        self.personnel = Personnel.objects.create(
            nom='Diallo',
            prenom='Mamadou',
            telephone='622111111',
            fonction='Maçon',
            type_contrat='Journalier',
            salaire_journalier=Decimal('50000.00'),
            salaire_convenu=Decimal('2000000.00'),
            actif=True
        )
    
    def test_validation_paiement_cree_transaction(self):
        """Test : La validation d'un paiement crée une transaction"""
        paiement = PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('500000.00'),
            mode_paiement='Espèces',
            statut='En_attente',
            saisi_par=self.user
        )
        
        # Vérifier qu'aucune transaction n'existe avant validation
        transactions_count_before = Transaction.objects.filter(
            projet=self.projet,
            type='Dépense',
            categorie='Paiement Personnel'
        ).count()
        self.assertEqual(transactions_count_before, 0)
        
        # Valider le paiement
        paiement.statut = 'Validé'
        paiement.save()
        
        # Vérifier qu'une transaction a été créée
        transactions_count_after = Transaction.objects.filter(
            projet=self.projet,
            type='Dépense',
            categorie='Paiement Personnel'
        ).count()
        self.assertEqual(transactions_count_after, 1)
        
        # Vérifier les détails de la transaction
        transaction = Transaction.objects.get(
            projet=self.projet,
            type='Dépense',
            categorie='Paiement Personnel'
        )
        self.assertEqual(transaction.montant, Decimal('500000.00'))
        self.assertEqual(transaction.statut, 'Validée')
    
    def test_paiement_deduit_du_budget_projet(self):
        """Test : Un paiement validé déduit du budget du projet"""
        # Créer un dépôt initial
        Transaction.objects.create(
            projet=self.projet,
            type='Dépôt',
            montant=Decimal('5000000.00'),
            date_transaction=date.today(),
            statut='Validée',
            saisi_par=self.user
        )
        
        budget_avant = self.projet.get_budget_disponible()
        
        # Créer et valider un paiement
        paiement = PaiementPersonnel.objects.create(
            personnel=self.personnel,
            projet=self.projet,
            date_paiement=date.today(),
            montant=Decimal('500000.00'),
            mode_paiement='Espèces',
            statut='En_attente',
            saisi_par=self.user
        )
        
        paiement.statut = 'Validé'
        paiement.save()
        
        # Vérifier que le budget a diminué
        budget_apres = self.projet.get_budget_disponible()
        self.assertEqual(budget_apres, budget_avant - Decimal('500000.00'))
