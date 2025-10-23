from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator


class Transaction(models.Model):
    """
    Modèle pour gérer les dépôts et retraits sur projets
    """
    TYPE_CHOICES = [
        ('Dépôt', 'Dépôt'),
        ('Retrait', 'Retrait'),
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('Espèces', 'Espèces'),
        ('Chèque', 'Chèque'),
        ('Virement', 'Virement'),
        ('Mobile_Money', 'Mobile Money'),
    ]
    
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Projet'
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name='Type'
    )
    montant = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Montant'
    )
    date_transaction = models.DateField(
        verbose_name='Date de transaction'
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Référence'
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        verbose_name='Mode de paiement'
    )
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='transactions_saisies',
        verbose_name='Saisi par'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    piece_justificative = models.FileField(
        upload_to='transactions/',
        blank=True,
        null=True,
        verbose_name='Pièce justificative'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date_transaction', '-date_creation']
        indexes = [
            models.Index(fields=['projet']),
            models.Index(fields=['type']),
            models.Index(fields=['date_transaction']),
        ]
    
    def __str__(self):
        return f"{self.type} - {self.montant} GNF - {self.projet.code_projet}"
    
    def get_absolute_url(self):
        return reverse('finances:transaction_detail', kwargs={'pk': self.pk})


class CategorieDepense(models.Model):
    """
    Modèle pour les catégories de dépenses
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
    couleur_hex = models.CharField(
        max_length=7,
        default='#6B7280',
        verbose_name='Couleur (hex)'
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
        verbose_name = 'Catégorie de dépense'
        verbose_name_plural = 'Catégories de dépenses'
        ordering = ['ordre_affichage', 'nom']
    
    def __str__(self):
        return self.nom
    
    def get_total_depenses(self):
        """Retourne le total des dépenses pour cette catégorie"""
        total = self.depenses.filter(statut='Validée').aggregate(
            total=models.Sum('montant')
        )['total']
        return total or 0


class Fournisseur(models.Model):
    """
    Modèle pour gérer les fournisseurs
    """
    TYPE_CHOICES = [
        ('Matériaux', 'Matériaux'),
        ('Equipement', 'Équipement'),
        ('Services', 'Services'),
        ('Transport', 'Transport'),
        ('Autre', 'Autre'),
    ]
    
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom'
    )
    contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Personne de contact'
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Téléphone'
    )
    telephone_2 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Téléphone 2'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )
    adresse = models.TextField(
        blank=True,
        null=True,
        verbose_name='Adresse'
    )
    ville = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ville'
    )
    nif = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='NIF'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='Autre',
        verbose_name='Type'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
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
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['type']),
        ]
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('finances:fournisseur_detail', kwargs={'pk': self.pk})
    
    def get_total_achats(self):
        """Retourne le total des achats auprès de ce fournisseur"""
        total = self.depenses.filter(statut='Validée').aggregate(
            total=models.Sum('montant')
        )['total']
        return total or 0


class Depense(models.Model):
    """
    Modèle pour gérer les dépenses de chantier
    """
    MODE_PAIEMENT_CHOICES = [
        ('Espèces', 'Espèces'),
        ('Chèque', 'Chèque'),
        ('Virement', 'Virement'),
        ('Mobile_Money', 'Mobile Money'),
    ]
    
    STATUT_CHOICES = [
        ('Validée', 'Validée'),
        ('En_attente', 'En attente'),
        ('Rejetée', 'Rejetée'),
    ]
    
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='depenses',
        verbose_name='Projet'
    )
    categorie = models.ForeignKey(
        CategorieDepense,
        on_delete=models.RESTRICT,
        related_name='depenses',
        verbose_name='Catégorie'
    )
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='depenses',
        verbose_name='Fournisseur'
    )
    date_depense = models.DateField(
        verbose_name='Date de dépense'
    )
    montant = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Montant'
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        verbose_name='Mode de paiement'
    )
    numero_facture = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='N° facture'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    piece_justificative = models.FileField(
        upload_to='depenses/',
        blank=True,
        null=True,
        verbose_name='Pièce justificative'
    )
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='depenses_saisies',
        verbose_name='Saisi par'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='En_attente',
        verbose_name='Statut'
    )
    date_validation = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de validation'
    )
    validee_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='depenses_validees',
        verbose_name='Validée par'
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
        verbose_name = 'Dépense'
        verbose_name_plural = 'Dépenses'
        ordering = ['-date_depense', '-date_creation']
        indexes = [
            models.Index(fields=['projet']),
            models.Index(fields=['categorie']),
            models.Index(fields=['date_depense']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"{self.categorie.nom} - {self.montant} GNF - {self.projet.code_projet}"
    
    def get_absolute_url(self):
        return reverse('finances:depense_detail', kwargs={'pk': self.pk})
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'Validée': 'bg-success',
            'En_attente': 'bg-warning',
            'Rejetée': 'bg-danger',
        }
        return statut_classes.get(self.statut, 'bg-secondary')
