from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import Sum, Q
from datetime import datetime


class UniteMessure(models.Model):
    """
    Modèle pour les unités de mesure (kg, m, m², pièce, etc.)
    """
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nom'
    )
    symbole = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Symbole'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Unité de mesure'
        verbose_name_plural = 'Unités de mesure'
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.symbole})"


class CategorieProduit(models.Model):
    """
    Modèle pour les catégories de produits
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nom'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Code'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name='Ordre d\'affichage'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Catégorie de produit'
        verbose_name_plural = 'Catégories de produits'
        ordering = ['ordre_affichage', 'nom']
    
    def __str__(self):
        return self.nom


class Produit(models.Model):
    """
    Modèle pour les produits/matériaux
    """
    code_produit = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Code produit',
        help_text='Généré automatiquement'
    )
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom du produit'
    )
    categorie = models.ForeignKey(
        CategorieProduit,
        on_delete=models.RESTRICT,
        related_name='produits',
        verbose_name='Catégorie'
    )
    unite_mesure = models.ForeignKey(
        UniteMessure,
        on_delete=models.RESTRICT,
        related_name='produits',
        verbose_name='Unité de mesure'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    prix_unitaire_moyen = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Prix unitaire moyen',
        help_text='Calculé automatiquement'
    )
    stock_minimum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Stock minimum',
        help_text='Seuil d\'alerte'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['code_produit']),
            models.Index(fields=['categorie']),
            models.Index(fields=['nom']),
        ]
    
    def __str__(self):
        return f"{self.code_produit} - {self.nom}"
    
    def save(self, *args, **kwargs):
        if not self.code_produit:
            # Génération automatique du code produit
            year = datetime.now().year
            last_produit = Produit.objects.filter(
                code_produit__startswith=f'PROD-{year}-'
            ).order_by('code_produit').last()
            
            if last_produit:
                last_number = int(last_produit.code_produit.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.code_produit = f'PROD-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('inventory:produit_detail', kwargs={'pk': self.pk})
    
    def get_stock_total(self):
        """Retourne le stock total tous projets confondus"""
        total = self.stocks.aggregate(total=Sum('quantite_actuelle'))['total']
        return total or 0
    
    def get_stock_projet(self, projet):
        """Retourne le stock pour un projet spécifique"""
        try:
            stock = self.stocks.get(projet=projet)
            return stock.quantite_actuelle
        except Stock.DoesNotExist:
            return 0
    
    def is_stock_faible(self, projet=None):
        """Vérifie si le stock est en dessous du minimum"""
        if projet:
            stock = self.get_stock_projet(projet)
        else:
            stock = self.get_stock_total()
        return stock < self.stock_minimum
    
    def get_projets_avec_stock_faible(self):
        """Retourne la liste des projets avec stock faible"""
        projets = []
        for stock in self.stocks.all():
            if stock.quantite_actuelle < self.stock_minimum:
                projets.append(stock.projet)
        return projets


class Stock(models.Model):
    """
    Modèle pour gérer le stock par projet
    """
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='stocks',
        verbose_name='Projet'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='stocks',
        verbose_name='Produit'
    )
    quantite_actuelle = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Quantité actuelle'
    )
    valeur_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Valeur du stock',
        help_text='Calculé automatiquement'
    )
    emplacement = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Emplacement'
    )
    date_derniere_entree = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Dernière entrée'
    )
    date_derniere_sortie = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Dernière sortie'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['projet', 'produit']
        unique_together = ['projet', 'produit']
        indexes = [
            models.Index(fields=['projet']),
            models.Index(fields=['produit']),
        ]
    
    def __str__(self):
        return f"{self.produit.nom} - {self.projet.code_projet} ({self.quantite_actuelle} {self.produit.unite_mesure.symbole})"
    
    def get_absolute_url(self):
        return reverse('inventory:stock_detail', kwargs={'pk': self.pk})
    
    def is_stock_faible(self):
        """Vérifie si le stock est en dessous du minimum"""
        return self.quantite_actuelle < self.produit.stock_minimum
    
    def calculer_valeur_stock(self):
        """Calcule la valeur du stock"""
        self.valeur_stock = self.quantite_actuelle * self.produit.prix_unitaire_moyen
        return self.valeur_stock


class Achat(models.Model):
    """
    Modèle pour gérer les achats de produits
    """
    STATUT_CHOICES = [
        ('Brouillon', 'Brouillon'),
        ('Validé', 'Validé'),
        ('Reçu', 'Reçu'),
        ('Annulé', 'Annulé'),
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('Espèces', 'Espèces'),
        ('Chèque', 'Chèque'),
        ('Virement', 'Virement'),
        ('Mobile_Money', 'Mobile Money'),
        ('Crédit', 'Crédit'),
    ]
    
    numero_achat = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='N° d\'achat',
        help_text='Généré automatiquement'
    )
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='achats',
        verbose_name='Projet'
    )
    fournisseur = models.ForeignKey(
        'finances.Fournisseur',
        on_delete=models.RESTRICT,
        related_name='achats',
        verbose_name='Fournisseur'
    )
    date_achat = models.DateField(
        verbose_name='Date d\'achat'
    )
    date_reception = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de réception'
    )
    numero_facture = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='N° facture fournisseur'
    )
    montant_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Montant total',
        help_text='Calculé automatiquement'
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        verbose_name='Mode de paiement'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='Brouillon',
        verbose_name='Statut'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    piece_justificative = models.FileField(
        upload_to='achats/',
        blank=True,
        null=True,
        verbose_name='Pièce justificative'
    )
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='achats_saisis',
        verbose_name='Saisi par'
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='achats_valides',
        verbose_name='Validé par'
    )
    date_validation = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de validation'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    class Meta:
        verbose_name = 'Achat'
        verbose_name_plural = 'Achats'
        ordering = ['-date_achat', '-date_creation']
        indexes = [
            models.Index(fields=['numero_achat']),
            models.Index(fields=['projet']),
            models.Index(fields=['fournisseur']),
            models.Index(fields=['date_achat']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"{self.numero_achat} - {self.fournisseur.nom} - {self.montant_total} GNF"
    
    def save(self, *args, **kwargs):
        if not self.numero_achat:
            # Génération automatique du numéro d'achat
            year = datetime.now().year
            last_achat = Achat.objects.filter(
                numero_achat__startswith=f'ACH-{year}-'
            ).order_by('numero_achat').last()
            
            if last_achat:
                last_number = int(last_achat.numero_achat.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_achat = f'ACH-{year}-{new_number:04d}'
        
        # Déduire du budget du projet si l'achat est validé ou reçu
        if self.pk:  # Si l'achat existe déjà (modification)
            old_achat = Achat.objects.get(pk=self.pk)
            # Si le statut change vers Validé ou Reçu
            if old_achat.statut in ['Brouillon', 'Annulé'] and self.statut in ['Validé', 'Reçu']:
                # Créer une transaction de dépense pour déduire du budget
                from apps.finances.models import Transaction
                Transaction.objects.create(
                    projet=self.projet,
                    type='Dépense',
                    categorie='Achat Matériaux',
                    montant=self.montant_total,
                    description=f'Achat {self.numero_achat} - {self.fournisseur.nom} - {self.notes or ""}',
                    date_transaction=self.date_achat,
                    mode_paiement=self.mode_paiement if self.mode_paiement != 'Crédit' else 'Espèces',
                    statut='Validée'
                )
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('inventory:achat_detail', kwargs={'pk': self.pk})
    
    def calculer_montant_total(self):
        """Calcule le montant total de l'achat"""
        total = self.lignes.aggregate(total=Sum(models.F('quantite') * models.F('prix_unitaire')))['total']
        self.montant_total = total or 0
        return self.montant_total
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'Brouillon': 'bg-secondary',
            'Validé': 'bg-info',
            'Reçu': 'bg-success',
            'Annulé': 'bg-danger',
        }
        return statut_classes.get(self.statut, 'bg-secondary')


class LigneAchat(models.Model):
    """
    Modèle pour les lignes d'achat (détail des produits achetés)
    """
    achat = models.ForeignKey(
        Achat,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Achat'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.RESTRICT,
        related_name='lignes_achat',
        verbose_name='Produit'
    )
    quantite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Quantité'
    )
    prix_unitaire = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix unitaire'
    )
    montant_ligne = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Montant',
        help_text='Calculé automatiquement'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Ligne d\'achat'
        verbose_name_plural = 'Lignes d\'achat'
        ordering = ['achat', 'id']
    
    def __str__(self):
        return f"{self.produit.nom} - {self.quantite} {self.produit.unite_mesure.symbole}"
    
    def save(self, *args, **kwargs):
        # Calcul du montant de la ligne
        self.montant_ligne = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
        
        # Mise à jour du montant total de l'achat
        self.achat.calculer_montant_total()
        self.achat.save()


class MouvementStock(models.Model):
    """
    Modèle pour tracer les mouvements de stock (entrées/sorties)
    """
    TYPE_CHOICES = [
        ('Entrée', 'Entrée'),
        ('Sortie', 'Sortie'),
        ('Ajustement', 'Ajustement'),
        ('Transfert', 'Transfert'),
    ]
    
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='mouvements',
        verbose_name='Stock'
    )
    type_mouvement = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Type de mouvement'
    )
    quantite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Quantité'
    )
    quantite_avant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Quantité avant'
    )
    quantite_apres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Quantité après'
    )
    date_mouvement = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date du mouvement'
    )
    achat = models.ForeignKey(
        Achat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mouvements_stock',
        verbose_name='Achat lié'
    )
    projet_destination = models.ForeignKey(
        'projects.Projet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mouvements_stock_recus',
        verbose_name='Projet destination',
        help_text='Pour les transferts'
    )
    motif = models.TextField(
        blank=True,
        null=True,
        verbose_name='Motif'
    )
    effectue_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='mouvements_stock_effectues',
        verbose_name='Effectué par'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Mouvement de stock'
        verbose_name_plural = 'Mouvements de stock'
        ordering = ['-date_mouvement']
        indexes = [
            models.Index(fields=['stock']),
            models.Index(fields=['type_mouvement']),
            models.Index(fields=['date_mouvement']),
        ]
    
    def __str__(self):
        return f"{self.type_mouvement} - {self.quantite} {self.stock.produit.unite_mesure.symbole} - {self.stock.produit.nom}"
    
    def save(self, *args, **kwargs):
        # Enregistrer la quantité avant
        self.quantite_avant = self.stock.quantite_actuelle
        
        # Mettre à jour le stock selon le type de mouvement
        if self.type_mouvement == 'Entrée':
            self.stock.quantite_actuelle += self.quantite
            self.stock.date_derniere_entree = self.date_mouvement
        elif self.type_mouvement == 'Sortie':
            self.stock.quantite_actuelle -= self.quantite
            self.stock.date_derniere_sortie = self.date_mouvement
        elif self.type_mouvement == 'Ajustement':
            # Pour l'ajustement, la quantité peut être positive ou négative
            self.stock.quantite_actuelle = self.quantite
        elif self.type_mouvement == 'Transfert':
            self.stock.quantite_actuelle -= self.quantite
            self.stock.date_derniere_sortie = self.date_mouvement
        
        # Enregistrer la quantité après
        self.quantite_apres = self.stock.quantite_actuelle
        
        # Recalculer la valeur du stock
        self.stock.calculer_valeur_stock()
        self.stock.save()
        
        super().save(*args, **kwargs)
