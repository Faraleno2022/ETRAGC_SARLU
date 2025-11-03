from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from apps.invoicing.models import Devis, LigneDevis
from apps.clients.models import Client
from apps.projects.models import Projet

User = get_user_model()


class DevisModelTest(TestCase):
    """Tests pour le modèle Devis"""
    
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
    
    def test_statuts_disponibles(self):
        """Test : Vérifier que tous les statuts sont disponibles"""
        statuts_attendus = ['Brouillon', 'Envoyé', 'Accepté', 'Refusé', 'Expiré', 'Gagné', 'Perdu']
        statuts_modele = [choice[0] for choice in Devis.STATUT_CHOICES]
        
        for statut in statuts_attendus:
            self.assertIn(statut, statuts_modele)
    
    def test_tva_optionnelle_active(self):
        """Test : TVA appliquée quand appliquer_tva=True"""
        devis = Devis.objects.create(
            client=self.client,
            projet=self.projet,
            date_emission=date.today(),
            date_validite=date.today() + timedelta(days=30),
            montant_ht=Decimal('1000000.00'),
            appliquer_tva=True,
            taux_tva=Decimal('18.00'),
            cree_par=self.user
        )
        
        # Vérifier le calcul de la TVA
        montant_tva_attendu = Decimal('1000000.00') * Decimal('0.18')
        self.assertEqual(devis.montant_tva, montant_tva_attendu)
        
        # Vérifier le montant TTC
        montant_ttc_attendu = Decimal('1000000.00') + montant_tva_attendu
        self.assertEqual(devis.montant_ttc, montant_ttc_attendu)
    
    def test_tva_optionnelle_desactive(self):
        """Test : TVA non appliquée quand appliquer_tva=False"""
        devis = Devis.objects.create(
            client=self.client,
            projet=self.projet,
            date_emission=date.today(),
            date_validite=date.today() + timedelta(days=30),
            montant_ht=Decimal('1000000.00'),
            appliquer_tva=False,
            taux_tva=Decimal('18.00'),
            cree_par=self.user
        )
        
        # Vérifier que la TVA est à 0
        self.assertEqual(devis.montant_tva, Decimal('0'))
        
        # Vérifier que le montant TTC = montant HT
        self.assertEqual(devis.montant_ttc, Decimal('1000000.00'))
    
    def test_tva_sans_taux(self):
        """Test : TVA à 0 quand taux_tva est None"""
        devis = Devis.objects.create(
            client=self.client,
            projet=self.projet,
            date_emission=date.today(),
            date_validite=date.today() + timedelta(days=30),
            montant_ht=Decimal('1000000.00'),
            appliquer_tva=True,
            taux_tva=None,
            cree_par=self.user
        )
        
        # Vérifier que la TVA est à 0
        self.assertEqual(devis.montant_tva, Decimal('0'))
        
        # Vérifier que le montant TTC = montant HT
        self.assertEqual(devis.montant_ttc, Decimal('1000000.00'))
    
    def test_changement_statut_gagne(self):
        """Test : Changement de statut vers 'Gagné'"""
        devis = Devis.objects.create(
            client=self.client,
            projet=self.projet,
            date_emission=date.today(),
            date_validite=date.today() + timedelta(days=30),
            montant_ht=Decimal('1000000.00'),
            statut='Envoyé',
            cree_par=self.user
        )
        
        # Changer le statut
        devis.statut = 'Gagné'
        devis.save()
        
        # Vérifier le changement
        devis.refresh_from_db()
        self.assertEqual(devis.statut, 'Gagné')
    
    def test_changement_statut_perdu(self):
        """Test : Changement de statut vers 'Perdu'"""
        devis = Devis.objects.create(
            client=self.client,
            projet=self.projet,
            date_emission=date.today(),
            date_validite=date.today() + timedelta(days=30),
            montant_ht=Decimal('1000000.00'),
            statut='Envoyé',
            cree_par=self.user
        )
        
        # Changer le statut
        devis.statut = 'Perdu'
        devis.save()
        
        # Vérifier le changement
        devis.refresh_from_db()
        self.assertEqual(devis.statut, 'Perdu')
    
    def test_generation_numero_devis(self):
        """Test : Génération automatique du numéro de devis"""
        devis = Devis.objects.create(
            client=self.client,
            projet=self.projet,
            date_emission=date.today(),
            date_validite=date.today() + timedelta(days=30),
            montant_ht=Decimal('1000000.00'),
            cree_par=self.user
        )
        
        # Vérifier que le numéro a été généré
        self.assertIsNotNone(devis.numero_devis)
        self.assertTrue(devis.numero_devis.startswith('DEV-'))
    
    def test_badge_class_statuts(self):
        """Test : Classes CSS des badges pour tous les statuts"""
        statuts_badges = {
            'Brouillon': 'bg-secondary',
            'Envoyé': 'bg-info',
            'Accepté': 'bg-success',
            'Refusé': 'bg-danger',
            'Expiré': 'bg-warning',
            'Gagné': 'bg-success',
            'Perdu': 'bg-danger',
        }
        
        for statut, badge_attendu in statuts_badges.items():
            devis = Devis.objects.create(
                client=self.client,
                projet=self.projet,
                date_emission=date.today(),
                date_validite=date.today() + timedelta(days=30),
                montant_ht=Decimal('1000000.00'),
                statut=statut,
                cree_par=self.user
            )
            
            self.assertEqual(devis.get_statut_badge_class(), badge_attendu)
