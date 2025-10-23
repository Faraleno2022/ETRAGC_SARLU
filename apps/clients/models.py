from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Client(models.Model):
    """
    Modèle pour gérer les clients d'ETRAGC
    """
    nom_complet = models.CharField(
        max_length=200,
        verbose_name='Nom complet'
    )
    entreprise = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Entreprise'
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
    pays = models.CharField(
        max_length=100,
        default='Guinée',
        verbose_name='Pays'
    )
    nif = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='NIF'
    )
    rccm = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='RCCM'
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
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['nom_complet']
        indexes = [
            models.Index(fields=['nom_complet']),
            models.Index(fields=['entreprise']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        if self.entreprise:
            return f"{self.nom_complet} - {self.entreprise}"
        return self.nom_complet
    
    def get_absolute_url(self):
        return reverse('clients:detail', kwargs={'pk': self.pk})
    
    def get_projets_count(self):
        """Retourne le nombre de projets du client"""
        return self.projets.count()
    
    def get_projets_actifs_count(self):
        """Retourne le nombre de projets actifs du client"""
        return self.projets.filter(statut='En_cours').count()
    
    def get_total_factures(self):
        """Retourne le montant total des factures du client"""
        from apps.invoicing.models import Facture
        total = Facture.objects.filter(client=self).aggregate(
            total=models.Sum('montant_ttc')
        )['total']
        return total or 0
    
    def get_factures_impayees(self):
        """Retourne le montant des factures impayées"""
        from apps.invoicing.models import Facture
        total = Facture.objects.filter(
            client=self
        ).exclude(
            statut_paiement='Payée'
        ).aggregate(
            total=models.Sum('montant_restant')
        )['total']
        return total or 0
