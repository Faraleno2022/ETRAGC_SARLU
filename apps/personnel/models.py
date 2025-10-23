from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator


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
