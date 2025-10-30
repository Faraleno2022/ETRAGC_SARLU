from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.conf import settings


class Personnel(models.Model):
    """
    Modèle pour gérer le personnel de chantier
    """
    FONCTION_CHOICES = [
        ('Ingénieur', 'Ingénieur'),
        ('Chef_Chantier', 'Chef de Chantier'),
        ('Maçon', 'Maçon'),
        ('Ferrailleur', 'Ferrailleur'),
        ('Électricien', 'Électricien'),
        ('Plombier', 'Plombier'),
        ('Charpentier', 'Charpentier'),
        ('Chauffeur', 'Chauffeur'),
        ('Gardien', 'Gardien'),
        ('Autre', 'Autre'),
    ]
    
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Journalier', 'Journalier'),
        ('Prestataire', 'Prestataire'),
    ]
    
    nom = models.CharField(
        max_length=100,
        verbose_name='Nom'
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name='Prénom'
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
    fonction = models.CharField(
        max_length=20,
        choices=FONCTION_CHOICES,
        verbose_name='Fonction'
    )
    type_contrat = models.CharField(
        max_length=20,
        choices=TYPE_CONTRAT_CHOICES,
        verbose_name='Type de contrat'
    )
    salaire_journalier = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name='Salaire journalier'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    date_embauche = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date d\'embauche'
    )
    date_fin_contrat = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de fin de contrat'
    )
    photo = models.ImageField(
        upload_to='personnel/',
        blank=True,
        null=True,
        verbose_name='Photo'
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
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    class Meta:
        verbose_name = 'Personnel'
        verbose_name_plural = 'Personnel'
        ordering = ['nom', 'prenom']
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['fonction']),
            models.Index(fields=['actif']),
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_fonction_display()}"
    
    def get_absolute_url(self):
        return reverse('personnel:detail', kwargs={'pk': self.pk})
    
    def get_full_name(self):
        """Retourne le nom complet"""
        return f"{self.prenom} {self.nom}"
    
    def get_projets_actifs(self):
        """Retourne les projets actifs auxquels le personnel est affecté"""
        return self.affectations.filter(
            date_fin__isnull=True,
            projet__statut='En_cours'
        )
    
    def is_disponible(self):
        """Vérifie si le personnel est disponible"""
        return self.actif and not self.get_projets_actifs().exists()
    
    def get_total_paiements(self, projet=None):
        """Retourne le total des paiements validés"""
        paiements = self.paiements.filter(statut='Validé')
        if projet:
            paiements = paiements.filter(projet=projet)
        total = paiements.aggregate(total=models.Sum('montant'))['total']
        return total or 0
    
    def get_salaire_du(self, projet=None):
        """Calcule le salaire dû basé sur les jours travaillés (affectations)"""
        from decimal import Decimal
        from datetime import date
        
        if not self.salaire_journalier:
            return Decimal('0')
        
        affectations = self.affectations.all()
        if projet:
            affectations = affectations.filter(projet=projet)
        
        total_jours = 0
        for affectation in affectations:
            if affectation.date_fin:
                jours = (affectation.date_fin - affectation.date_debut).days + 1
            else:
                jours = (date.today() - affectation.date_debut).days + 1
            total_jours += jours
        
        return Decimal(str(total_jours)) * self.salaire_journalier
    
    def get_reste_a_payer(self, projet=None):
        """Calcule le reste à payer (salaire dû - paiements reçus)"""
        salaire_du = self.get_salaire_du(projet)
        total_paye = self.get_total_paiements(projet)
        return salaire_du - total_paye
    
    def get_paiements_par_projet(self):
        """Retourne un dictionnaire des paiements groupés par projet"""
        from django.db.models import Sum
        from collections import defaultdict
        
        resultats = []
        projets_ids = self.affectations.values_list('projet_id', flat=True).distinct()
        
        for projet_id in projets_ids:
            from apps.projects.models import Projet
            try:
                projet = Projet.objects.get(pk=projet_id)
                salaire_du = self.get_salaire_du(projet)
                total_paye = self.get_total_paiements(projet)
                reste = salaire_du - total_paye
                
                resultats.append({
                    'projet': projet,
                    'salaire_du': salaire_du,
                    'total_paye': total_paye,
                    'reste_a_payer': reste,
                })
            except Projet.DoesNotExist:
                pass
        
        return resultats


class AffectationPersonnel(models.Model):
    """
    Modèle pour gérer l'affectation du personnel aux projets
    """
    ROLE_CHANTIER_CHOICES = [
        ('Chef', 'Chef'),
        ('Superviseur', 'Superviseur'),
        ('Ouvrier', 'Ouvrier'),
        ('Technicien', 'Technicien'),
        ('Support', 'Support'),
    ]
    
    personnel = models.ForeignKey(
        Personnel,
        on_delete=models.CASCADE,
        related_name='affectations',
        verbose_name='Personnel'
    )
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='affectations_personnel',
        verbose_name='Projet'
    )
    date_debut = models.DateField(
        verbose_name='Date de début'
    )
    date_fin = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de fin'
    )
    role_chantier = models.CharField(
        max_length=20,
        choices=ROLE_CHANTIER_CHOICES,
        default='Ouvrier',
        verbose_name='Rôle sur le chantier'
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
        verbose_name = 'Affectation de personnel'
        verbose_name_plural = 'Affectations de personnel'
        ordering = ['-date_debut']
        unique_together = ['personnel', 'projet', 'date_debut']
        indexes = [
            models.Index(fields=['personnel']),
            models.Index(fields=['projet']),
            models.Index(fields=['date_debut', 'date_fin']),
        ]
    
    def __str__(self):
        return f"{self.personnel.get_full_name()} - {self.projet.code_projet}"
    
    def get_duree_jours(self):
        """Retourne la durée de l'affectation en jours"""
        if self.date_fin:
            return (self.date_fin - self.date_debut).days
        else:
            from datetime import date
            return (date.today() - self.date_debut).days
    
    def is_active(self):
        """Vérifie si l'affectation est active"""
        from datetime import date
        if self.date_fin:
            return self.date_debut <= date.today() <= self.date_fin
        return self.date_debut <= date.today()


class PaiementPersonnel(models.Model):
    """
    Modèle pour gérer les paiements du personnel sur les projets
    """
    MODE_PAIEMENT_CHOICES = [
        ('Espèces', 'Espèces'),
        ('Chèque', 'Chèque'),
        ('Virement', 'Virement'),
        ('Mobile_Money', 'Mobile Money'),
    ]
    
    STATUT_CHOICES = [
        ('Validé', 'Validé'),
        ('En_attente', 'En attente'),
        ('Rejeté', 'Rejeté'),
    ]
    
    personnel = models.ForeignKey(
        Personnel,
        on_delete=models.CASCADE,
        related_name='paiements',
        verbose_name='Personnel'
    )
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='paiements_personnel',
        verbose_name='Projet'
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
    nombre_jours = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name='Nombre de jours',
        help_text='Pour les journaliers'
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        default='Espèces',
        verbose_name='Mode de paiement'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='En_attente',
        verbose_name='Statut'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    piece_justificative = models.FileField(
        upload_to='paiements_personnel/',
        blank=True,
        null=True,
        verbose_name='Pièce justificative'
    )
    saisi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='paiements_personnel_saisis',
        verbose_name='Saisi par'
    )
    date_validation = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de validation'
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiements_personnel_valides',
        verbose_name='Validé par'
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
        verbose_name = 'Paiement de personnel'
        verbose_name_plural = 'Paiements de personnel'
        ordering = ['-date_paiement', '-date_creation']
        indexes = [
            models.Index(fields=['personnel']),
            models.Index(fields=['projet']),
            models.Index(fields=['date_paiement']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"{self.personnel.get_full_name()} - {self.montant} GNF - {self.projet.code_projet}"
    
    def save(self, *args, **kwargs):
        # Déduire du budget du projet si le paiement est validé
        if self.pk:  # Si le paiement existe déjà (modification)
            old_paiement = PaiementPersonnel.objects.get(pk=self.pk)
            # Si le statut change vers Validé
            if old_paiement.statut != 'Validé' and self.statut == 'Validé':
                # Créer une transaction de dépense pour déduire du budget
                from apps.finances.models import Transaction
                Transaction.objects.create(
                    projet=self.projet,
                    type='Dépense',
                    categorie='Paiement Personnel',
                    montant=self.montant,
                    description=f'Paiement {self.personnel.get_full_name()} - {self.description or ""}',
                    date_transaction=self.date_paiement,
                    mode_paiement=self.mode_paiement,
                    statut='Validée'
                )
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('personnel:paiement_detail', kwargs={'pk': self.pk})
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'Validé': 'bg-success',
            'En_attente': 'bg-warning',
            'Rejeté': 'bg-danger',
        }
        return statut_classes.get(self.statut, 'bg-secondary')
