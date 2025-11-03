from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta
from decimal import Decimal


class Devis(models.Model):
    """
    Modèle pour gérer les devis pro forma
    """
    STATUT_CHOICES = [
        ('Brouillon', 'Brouillon'),
        ('Envoyé', 'Envoyé'),
        ('Accepté', 'Accepté'),
        ('Refusé', 'Refusé'),
        ('Expiré', 'Expiré'),
        ('Gagné', 'Gagné'),
        ('Perdu', 'Perdu'),
    ]
    
    numero_devis = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='N° devis',
        help_text='Généré automatiquement'
    )
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='devis',
        verbose_name='Projet'
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.RESTRICT,
        related_name='devis',
        verbose_name='Client'
    )
    date_emission = models.DateField(
        verbose_name='Date d\'émission'
    )
    date_validite = models.DateField(
        verbose_name='Date de validité'
    )
    montant_ht = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name='Montant HT'
    )
    appliquer_tva = models.BooleanField(
        default=True,
        verbose_name='Appliquer la TVA'
    )
    taux_tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00,
        blank=True,
        null=True,
        verbose_name='Taux TVA (%)'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='Brouillon',
        verbose_name='Statut'
    )
    conditions_paiement = models.TextField(
        blank=True,
        null=True,
        verbose_name='Conditions de paiement'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='devis_crees',
        verbose_name='Créé par'
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
        verbose_name = 'Devis'
        verbose_name_plural = 'Devis'
        ordering = ['-date_emission', '-date_creation']
        indexes = [
            models.Index(fields=['numero_devis']),
            models.Index(fields=['client']),
            models.Index(fields=['statut']),
            models.Index(fields=['date_emission']),
        ]
    
    def __str__(self):
        return f"{self.numero_devis} - {self.client.nom_complet}"
    
    def save(self, *args, **kwargs):
        if not self.numero_devis:
            # Génération automatique du numéro de devis
            year = datetime.now().year
            last_devis = Devis.objects.filter(
                numero_devis__startswith=f'DEV-{year}-'
            ).order_by('numero_devis').last()
            
            if last_devis:
                last_number = int(last_devis.numero_devis.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_devis = f'DEV-{year}-{new_number:03d}'
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('invoicing:devis_detail', kwargs={'pk': self.pk})
    
    @property
    def montant_tva(self):
        """Calcule le montant de la TVA"""
        if self.appliquer_tva and self.taux_tva:
            return self.montant_ht * (Decimal(str(self.taux_tva)) / Decimal('100'))
        return Decimal('0')
    
    @property
    def montant_ttc(self):
        """Calcule le montant TTC"""
        return self.montant_ht + self.montant_tva
    
    def is_expire(self):
        """Vérifie si le devis est expiré"""
        from datetime import date
        return date.today() > self.date_validite
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'Brouillon': 'bg-secondary',
            'Envoyé': 'bg-info',
            'Accepté': 'bg-success',
            'Refusé': 'bg-danger',
            'Expiré': 'bg-warning',
            'Gagné': 'bg-success',
            'Perdu': 'bg-danger',
        }
        return statut_classes.get(self.statut, 'bg-secondary')
    
    def calculer_montant_total(self):
        """Recalcule le montant HT à partir des lignes"""
        if self.pk:
            total = sum((ligne.montant_ht for ligne in self.lignes.all()), Decimal('0'))
            self.montant_ht = total
            self.save()


class LigneDevis(models.Model):
    """
    Modèle pour les lignes de détail d'un devis
    """
    devis = models.ForeignKey(
        Devis,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Devis'
    )
    ordre = models.IntegerField(
        default=1,
        verbose_name='Ordre'
    )
    designation = models.CharField(
        max_length=255,
        verbose_name='Désignation'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    quantite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.00,
        validators=[MinValueValidator(0.01)],
        verbose_name='Quantité'
    )
    unite = models.CharField(
        max_length=20,
        default='Forfait',
        verbose_name='Unité'
    )
    prix_unitaire_ht = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix unitaire HT'
    )
    
    class Meta:
        verbose_name = 'Ligne de devis'
        verbose_name_plural = 'Lignes de devis'
        ordering = ['ordre']
    
    def __str__(self):
        return f"{self.designation} - {self.devis.numero_devis}"
    
    @property
    def montant_ht(self):
        """Calcule le montant HT de la ligne"""
        return Decimal(str(self.quantite)) * Decimal(str(self.prix_unitaire_ht))
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Facture(models.Model):
    """
    Modèle pour gérer les factures clients
    """
    STATUT_PAIEMENT_CHOICES = [
        ('Impayée', 'Impayée'),
        ('Partielle', 'Partielle'),
        ('Payée', 'Payée'),
        ('En_retard', 'En retard'),
    ]
    
    numero_facture = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='N° facture',
        help_text='Généré automatiquement'
    )
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='factures',
        verbose_name='Projet'
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.RESTRICT,
        related_name='factures',
        verbose_name='Client'
    )
    devis = models.ForeignKey(
        Devis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='factures',
        verbose_name='Devis'
    )
    date_emission = models.DateField(
        verbose_name='Date d\'émission'
    )
    date_echeance = models.DateField(
        verbose_name='Date d\'échéance'
    )
    montant_ht = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name='Montant HT'
    )
    taux_tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00,
        verbose_name='Taux TVA (%)'
    )
    montant_paye = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name='Montant payé'
    )
    statut_paiement = models.CharField(
        max_length=20,
        choices=STATUT_PAIEMENT_CHOICES,
        default='Impayée',
        verbose_name='Statut de paiement'
    )
    conditions_paiement = models.TextField(
        blank=True,
        null=True,
        verbose_name='Conditions de paiement'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='factures_creees',
        verbose_name='Créé par'
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
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'
        ordering = ['-date_emission', '-date_creation']
        indexes = [
            models.Index(fields=['numero_facture']),
            models.Index(fields=['client']),
            models.Index(fields=['statut_paiement']),
            models.Index(fields=['date_emission']),
        ]
    
    def __str__(self):
        return f"{self.numero_facture} - {self.client.nom_complet}"
    
    def save(self, *args, **kwargs):
        if not self.numero_facture:
            # Génération automatique du numéro de facture
            year = datetime.now().year
            last_facture = Facture.objects.filter(
                numero_facture__startswith=f'FACT-{year}-'
            ).order_by('numero_facture').last()
            
            if last_facture:
                last_number = int(last_facture.numero_facture.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_facture = f'FACT-{year}-{new_number:03d}'
        
        # Mise à jour du statut de paiement
        if self.montant_paye >= self.montant_ttc:
            self.statut_paiement = 'Payée'
        elif self.montant_paye > 0:
            self.statut_paiement = 'Partielle'
        elif self.is_en_retard():
            self.statut_paiement = 'En_retard'
        else:
            self.statut_paiement = 'Impayée'
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('invoicing:facture_detail', kwargs={'pk': self.pk})
    
    @property
    def montant_tva(self):
        """Calcule le montant de la TVA"""
        return self.montant_ht * (Decimal(str(self.taux_tva)) / Decimal('100'))
    
    @property
    def montant_ttc(self):
        """Calcule le montant TTC"""
        return self.montant_ht + self.montant_tva
    
    @property
    def montant_restant(self):
        """Calcule le montant restant à payer"""
        return self.montant_ttc - self.montant_paye
    
    def is_en_retard(self):
        """Vérifie si la facture est en retard"""
        from datetime import date
        return date.today() > self.date_echeance and self.statut_paiement != 'Payée'
    
    def get_jours_retard(self):
        """Retourne le nombre de jours de retard"""
        if self.is_en_retard():
            from datetime import date
            return (date.today() - self.date_echeance).days
        return 0
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'Impayée': 'bg-warning',
            'Partielle': 'bg-info',
            'Payée': 'bg-success',
            'En_retard': 'bg-danger',
        }
        return statut_classes.get(self.statut_paiement, 'bg-secondary')
    
    def calculer_montant_total(self):
        """Recalcule le montant HT à partir des lignes"""
        if self.pk:
            total = sum((ligne.montant_ht for ligne in self.lignes.all()), Decimal('0'))
            self.montant_ht = total
            self.save()
    
    def mettre_a_jour_statut_paiement(self):
        """Met à jour le statut de paiement en fonction du montant payé"""
        if self.montant_paye >= self.montant_ttc:
            self.statut_paiement = 'Payée'
        elif self.montant_paye > 0:
            self.statut_paiement = 'Partielle'
        elif self.is_en_retard():
            self.statut_paiement = 'En_retard'
        else:
            self.statut_paiement = 'Impayée'
        self.save()


class LigneFacture(models.Model):
    """
    Modèle pour les lignes de détail d'une facture
    """
    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Facture'
    )
    ordre = models.IntegerField(
        default=1,
        verbose_name='Ordre'
    )
    designation = models.CharField(
        max_length=255,
        verbose_name='Désignation'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    quantite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.00,
        validators=[MinValueValidator(0.01)],
        verbose_name='Quantité'
    )
    unite = models.CharField(
        max_length=20,
        default='Forfait',
        verbose_name='Unité'
    )
    prix_unitaire_ht = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix unitaire HT'
    )
    
    class Meta:
        verbose_name = 'Ligne de facture'
        verbose_name_plural = 'Lignes de factures'
        ordering = ['ordre']
    
    def __str__(self):
        return f"{self.designation} - {self.facture.numero_facture}"
    
    @property
    def montant_ht(self):
        """Calcule le montant HT de la ligne"""
        return Decimal(str(self.quantite)) * Decimal(str(self.prix_unitaire_ht))
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PaiementFacture(models.Model):
    """
    Modèle pour suivre les paiements reçus sur factures
    """
    MODE_PAIEMENT_CHOICES = [
        ('Espèces', 'Espèces'),
        ('Chèque', 'Chèque'),
        ('Virement', 'Virement'),
        ('Mobile_Money', 'Mobile Money'),
    ]
    
    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name='paiements',
        verbose_name='Facture'
    )
    date_paiement = models.DateField(
        verbose_name='Date de paiement'
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
    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Référence'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    enregistre_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='paiements_enregistres',
        verbose_name='Enregistré par'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    class Meta:
        verbose_name = 'Paiement de facture'
        verbose_name_plural = 'Paiements de factures'
        ordering = ['-date_paiement', '-date_creation']
        indexes = [
            models.Index(fields=['facture']),
            models.Index(fields=['date_paiement']),
        ]
    
    def __str__(self):
        return f"Paiement {self.montant} GNF - {self.facture.numero_facture}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le montant payé de la facture
        total_paye = self.facture.paiements.aggregate(
            total=models.Sum('montant')
        )['total'] or 0
        self.facture.montant_paye = total_paye
        self.facture.save()
