from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from datetime import date

from .models import (
    UniteMessure, CategorieProduit, Produit, Stock,
    Achat, LigneAchat, MouvementStock
)
from apps.projects.models import Projet
from apps.finances.models import Fournisseur
from apps.clients.models import Client as ClientModel

User = get_user_model()


class UniteMessureModelTest(TestCase):
    """Tests pour le modèle UniteMessure"""
    
    def setUp(self):
        self.unite = UniteMessure.objects.create(
            nom='Kilogramme',
            symbole='kg',
            description='Unité de masse'
        )
    
    def test_unite_creation(self):
        """Test de création d'une unité de mesure"""
        self.assertEqual(self.unite.nom, 'Kilogramme')
        self.assertEqual(self.unite.symbole, 'kg')
        self.assertTrue(self.unite.actif)
    
    def test_unite_str(self):
        """Test de la représentation string"""
        self.assertEqual(str(self.unite), 'Kilogramme (kg)')


class ProduitModelTest(TestCase):
    """Tests pour le modèle Produit"""
    
    def setUp(self):
        self.unite = UniteMessure.objects.create(nom='Kilogramme', symbole='kg')
        self.categorie = CategorieProduit.objects.create(nom='Ciment', code='CIM')
        self.produit = Produit.objects.create(
            nom='Ciment CPJ 42.5',
            categorie=self.categorie,
            unite_mesure=self.unite,
            prix_unitaire_moyen=Decimal('50000.00'),
            stock_minimum=Decimal('10.00')
        )
    
    def test_produit_creation(self):
        """Test de création d'un produit"""
        self.assertEqual(self.produit.nom, 'Ciment CPJ 42.5')
        self.assertIsNotNone(self.produit.code_produit)
        self.assertTrue(self.produit.code_produit.startswith('PROD-'))
    
    def test_code_produit_auto_generation(self):
        """Test de génération automatique du code produit"""
        produit2 = Produit.objects.create(
            nom='Ciment Blanc',
            categorie=self.categorie,
            unite_mesure=self.unite
        )
        self.assertIsNotNone(produit2.code_produit)
        self.assertNotEqual(self.produit.code_produit, produit2.code_produit)
    
    def test_get_stock_total(self):
        """Test du calcul du stock total"""
        # Créer un client et un projet pour les tests
        client = ClientModel.objects.create(
            nom='Client Test',
            telephone='123456789'
        )
        projet = Projet.objects.create(
            nom_projet='Projet Test',
            client=client,
            montant_prevu=Decimal('1000000.00')
        )
        
        # Créer des stocks
        Stock.objects.create(
            projet=projet,
            produit=self.produit,
            quantite_actuelle=Decimal('50.00')
        )
        
        self.assertEqual(self.produit.get_stock_total(), Decimal('50.00'))


class StockModelTest(TestCase):
    """Tests pour le modèle Stock"""
    
    def setUp(self):
        # Créer les dépendances
        self.unite = UniteMessure.objects.create(nom='Kilogramme', symbole='kg')
        self.categorie = CategorieProduit.objects.create(nom='Ciment', code='CIM')
        self.produit = Produit.objects.create(
            nom='Ciment CPJ 42.5',
            categorie=self.categorie,
            unite_mesure=self.unite,
            prix_unitaire_moyen=Decimal('50000.00'),
            stock_minimum=Decimal('10.00')
        )
        
        client = ClientModel.objects.create(
            nom='Client Test',
            telephone='123456789'
        )
        self.projet = Projet.objects.create(
            nom_projet='Projet Test',
            client=client,
            montant_prevu=Decimal('1000000.00')
        )
        
        self.stock = Stock.objects.create(
            projet=self.projet,
            produit=self.produit,
            quantite_actuelle=Decimal('5.00')
        )
    
    def test_stock_creation(self):
        """Test de création d'un stock"""
        self.assertEqual(self.stock.quantite_actuelle, Decimal('5.00'))
        self.assertEqual(self.stock.projet, self.projet)
        self.assertEqual(self.stock.produit, self.produit)
    
    def test_is_stock_faible(self):
        """Test de détection de stock faible"""
        self.assertTrue(self.stock.is_stock_faible())
        
        self.stock.quantite_actuelle = Decimal('20.00')
        self.stock.save()
        self.assertFalse(self.stock.is_stock_faible())
    
    def test_calculer_valeur_stock(self):
        """Test du calcul de la valeur du stock"""
        valeur = self.stock.calculer_valeur_stock()
        expected = Decimal('5.00') * Decimal('50000.00')
        self.assertEqual(valeur, expected)


class AchatModelTest(TestCase):
    """Tests pour le modèle Achat"""
    
    def setUp(self):
        # Créer les dépendances
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        client = ClientModel.objects.create(
            nom='Client Test',
            telephone='123456789'
        )
        self.projet = Projet.objects.create(
            nom_projet='Projet Test',
            client=client,
            montant_prevu=Decimal('1000000.00')
        )
        
        self.fournisseur = Fournisseur.objects.create(
            nom='Fournisseur Test',
            telephone='987654321'
        )
        
        self.achat = Achat.objects.create(
            projet=self.projet,
            fournisseur=self.fournisseur,
            date_achat=date.today(),
            mode_paiement='Espèces',
            saisi_par=self.user
        )
    
    def test_achat_creation(self):
        """Test de création d'un achat"""
        self.assertIsNotNone(self.achat.numero_achat)
        self.assertTrue(self.achat.numero_achat.startswith('ACH-'))
        self.assertEqual(self.achat.statut, 'Brouillon')
    
    def test_numero_achat_auto_generation(self):
        """Test de génération automatique du numéro d'achat"""
        achat2 = Achat.objects.create(
            projet=self.projet,
            fournisseur=self.fournisseur,
            date_achat=date.today(),
            mode_paiement='Espèces',
            saisi_par=self.user
        )
        self.assertIsNotNone(achat2.numero_achat)
        self.assertNotEqual(self.achat.numero_achat, achat2.numero_achat)


class InventoryViewsTest(TestCase):
    """Tests pour les vues du module inventory"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_dashboard_view(self):
        """Test de la vue dashboard"""
        response = self.client.get(reverse('inventory:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/dashboard.html')
    
    def test_produit_list_view(self):
        """Test de la vue liste des produits"""
        response = self.client.get(reverse('inventory:produit_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/produit_list.html')
    
    def test_stock_list_view(self):
        """Test de la vue liste des stocks"""
        response = self.client.get(reverse('inventory:stock_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/stock_list.html')
    
    def test_achat_list_view(self):
        """Test de la vue liste des achats"""
        response = self.client.get(reverse('inventory:achat_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/achat_list.html')
    
    def test_alertes_view(self):
        """Test de la vue alertes"""
        response = self.client.get(reverse('inventory:alertes_stock'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/alertes_stock.html')
    
    def test_views_require_authentication(self):
        """Test que les vues nécessitent l'authentification"""
        self.client.logout()
        response = self.client.get(reverse('inventory:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login


class MouvementStockTest(TestCase):
    """Tests pour les mouvements de stock"""
    
    def setUp(self):
        # Créer les dépendances
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        self.unite = UniteMessure.objects.create(nom='Kilogramme', symbole='kg')
        self.categorie = CategorieProduit.objects.create(nom='Ciment', code='CIM')
        self.produit = Produit.objects.create(
            nom='Ciment CPJ 42.5',
            categorie=self.categorie,
            unite_mesure=self.unite,
            prix_unitaire_moyen=Decimal('50000.00'),
            stock_minimum=Decimal('10.00')
        )
        
        client = ClientModel.objects.create(
            nom='Client Test',
            telephone='123456789'
        )
        self.projet = Projet.objects.create(
            nom_projet='Projet Test',
            client=client,
            montant_prevu=Decimal('1000000.00')
        )
        
        self.stock = Stock.objects.create(
            projet=self.projet,
            produit=self.produit,
            quantite_actuelle=Decimal('20.00')
        )
    
    def test_mouvement_entree(self):
        """Test d'un mouvement d'entrée"""
        quantite_avant = self.stock.quantite_actuelle
        
        mouvement = MouvementStock.objects.create(
            stock=self.stock,
            type_mouvement='Entrée',
            quantite=Decimal('10.00'),
            motif='Test entrée',
            effectue_par=self.user
        )
        
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantite_actuelle, quantite_avant + Decimal('10.00'))
        self.assertEqual(mouvement.quantite_avant, quantite_avant)
        self.assertEqual(mouvement.quantite_apres, quantite_avant + Decimal('10.00'))
    
    def test_mouvement_sortie(self):
        """Test d'un mouvement de sortie"""
        quantite_avant = self.stock.quantite_actuelle
        
        mouvement = MouvementStock.objects.create(
            stock=self.stock,
            type_mouvement='Sortie',
            quantite=Decimal('5.00'),
            motif='Test sortie',
            effectue_par=self.user
        )
        
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantite_actuelle, quantite_avant - Decimal('5.00'))
