from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class Projet(models.Model):
    """
    Modèle pour gérer les projets de construction
    """
    STATUT_CHOICES = [
        ('Planifié', 'Planifié'),
        ('En_cours', 'En cours'),
        ('Suspendu', 'Suspendu'),
        ('Terminé', 'Terminé'),
        ('Annulé', 'Annulé'),
    ]
    
    code_projet = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Code projet',
        help_text='Généré automatiquement'
    )
    nom_projet = models.CharField(
        max_length=255,
        verbose_name='Nom du projet'
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.RESTRICT,
        related_name='projets',
        verbose_name='Client'
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projets_responsable',
        verbose_name='Responsable'
    )
    montant_prevu = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Montant prévu'
    )
    date_debut = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de début'
    )
    date_fin_prevue = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de fin prévue'
    )
    date_fin_reelle = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de fin réelle'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='Planifié',
        verbose_name='Statut'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    adresse_chantier = models.TextField(
        blank=True,
        null=True,
        verbose_name='Adresse du chantier'
    )
    ville_chantier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ville du chantier'
    )
    pourcentage_avancement = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Avancement (%)'
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
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['code_projet']),
            models.Index(fields=['statut']),
            models.Index(fields=['client']),
            models.Index(fields=['date_debut', 'date_fin_prevue']),
        ]
    
    def __str__(self):
        return f"{self.code_projet} - {self.nom_projet}"
    
    def save(self, *args, **kwargs):
        if not self.code_projet:
            # Génération automatique du code projet
            year = datetime.now().year
            last_projet = Projet.objects.filter(
                code_projet__startswith=f'PROJ-{year}-'
            ).order_by('code_projet').last()
            
            if last_projet:
                last_number = int(last_projet.code_projet.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.code_projet = f'PROJ-{year}-{new_number:03d}'
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk})
    
    def get_total_depots(self):
        """Retourne le total des dépôts"""
        from apps.finances.models import Transaction
        total = Transaction.objects.filter(
            projet=self,
            type='Dépôt'
        ).aggregate(total=models.Sum('montant'))['total']
        return total or 0
    
    def get_total_retraits(self):
        """Retourne le total des retraits"""
        from apps.finances.models import Transaction
        total = Transaction.objects.filter(
            projet=self,
            type='Retrait'
        ).aggregate(total=models.Sum('montant'))['total']
        return total or 0
    
    def get_solde_disponible(self):
        """Retourne le solde disponible"""
        return self.get_total_depots() - self.get_total_retraits()
    
    def get_total_depenses(self):
        """Retourne le total de toutes les dépenses (Dépenses + Achats + Retraits)"""
        from apps.finances.models import Transaction
        
        # Total des transactions de type Dépense et Retrait
        total_transactions = Transaction.objects.filter(
            projet=self,
            type__in=['Dépense', 'Retrait'],
            statut='Validée'
        ).aggregate(total=models.Sum('montant'))['total'] or 0
        
        return total_transactions
    
    def get_total_depots(self):
        """Retourne le total des dépôts"""
        from apps.finances.models import Transaction
        
        total = Transaction.objects.filter(
            projet=self,
            type='Dépôt',
            statut='Validée'
        ).aggregate(total=models.Sum('montant'))['total'] or 0
        
        return total
    
    def get_budget_disponible(self):
        """Retourne le budget disponible (Budget initial + Dépôts - Dépenses)"""
        return self.montant_prevu + self.get_total_depots() - self.get_total_depenses()
    
    def get_pourcentage_budget_consomme(self):
        """Retourne le pourcentage du budget consommé"""
        from decimal import Decimal
        budget_total = self.montant_prevu + self.get_total_depots()
        if budget_total > 0:
            return float((self.get_total_depenses() / budget_total) * Decimal('100'))
        return 0
    
    def is_budget_depasse(self):
        """Vérifie si le budget est dépassé"""
        return self.get_budget_disponible() < 0
    
    def get_duree_prevue_jours(self):
        """Retourne la durée prévue en jours"""
        if self.date_debut and self.date_fin_prevue:
            return (self.date_fin_prevue - self.date_debut).days
        return 0
    
    def get_duree_reelle_jours(self):
        """Retourne la durée réelle en jours"""
        if self.date_debut and self.date_fin_reelle:
            return (self.date_fin_reelle - self.date_debut).days
        return 0
    
    def is_en_retard(self):
        """Vérifie si le projet est en retard"""
        if self.date_fin_prevue and self.statut not in ['Terminé', 'Annulé']:
            from datetime import date
            return date.today() > self.date_fin_prevue
        return False
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'Planifié': 'bg-info',
            'En_cours': 'bg-primary',
            'Suspendu': 'bg-warning',
            'Terminé': 'bg-success',
            'Annulé': 'bg-danger',
        }
        return statut_classes.get(self.statut, 'bg-secondary')
