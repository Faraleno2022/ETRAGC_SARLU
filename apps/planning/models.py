from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Tache(models.Model):
    """
    Modèle pour gérer les tâches et le planning des projets
    """
    PRIORITE_CHOICES = [
        ('Basse', 'Basse'),
        ('Moyenne', 'Moyenne'),
        ('Haute', 'Haute'),
        ('Critique', 'Critique'),
    ]
    
    STATUT_CHOICES = [
        ('A_faire', 'À faire'),
        ('En_cours', 'En cours'),
        ('En_pause', 'En pause'),
        ('Terminée', 'Terminée'),
        ('Bloquée', 'Bloquée'),
        ('Annulée', 'Annulée'),
    ]
    
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        related_name='taches',
        verbose_name='Projet'
    )
    nom_tache = models.CharField(
        max_length=255,
        verbose_name='Nom de la tâche'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    date_debut = models.DateField(
        verbose_name='Date de début'
    )
    date_fin_prevue = models.DateField(
        verbose_name='Date de fin prévue'
    )
    date_fin_reelle = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de fin réelle'
    )
    priorite = models.CharField(
        max_length=20,
        choices=PRIORITE_CHOICES,
        default='Moyenne',
        verbose_name='Priorité'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='A_faire',
        verbose_name='Statut'
    )
    pourcentage_progression = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Progression (%)'
    )
    responsable = models.ForeignKey(
        'personnel.Personnel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taches_responsable',
        verbose_name='Responsable'
    )
    tache_parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sous_taches',
        verbose_name='Tâche parente'
    )
    ordre_affichage = models.IntegerField(
        default=0,
        verbose_name='Ordre d\'affichage'
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
        verbose_name = 'Tâche'
        verbose_name_plural = 'Tâches'
        ordering = ['ordre_affichage', 'date_debut']
        indexes = [
            models.Index(fields=['projet']),
            models.Index(fields=['statut']),
            models.Index(fields=['date_debut', 'date_fin_prevue']),
            models.Index(fields=['responsable']),
        ]
    
    def __str__(self):
        return f"{self.nom_tache} - {self.projet.code_projet}"
    
    def get_absolute_url(self):
        return reverse('planning:tache_detail', kwargs={'pk': self.pk})
    
    def get_duree_prevue_jours(self):
        """Retourne la durée prévue en jours"""
        return (self.date_fin_prevue - self.date_debut).days + 1
    
    def get_duree_reelle_jours(self):
        """Retourne la durée réelle en jours"""
        if self.date_fin_reelle:
            return (self.date_fin_reelle - self.date_debut).days + 1
        return 0
    
    def is_en_retard(self):
        """Vérifie si la tâche est en retard"""
        if self.statut not in ['Terminée', 'Annulée']:
            from datetime import date
            return date.today() > self.date_fin_prevue
        return False
    
    def get_jours_retard(self):
        """Retourne le nombre de jours de retard"""
        if self.is_en_retard():
            from datetime import date
            return (date.today() - self.date_fin_prevue).days
        return 0
    
    def get_statut_badge_class(self):
        """Retourne la classe CSS pour le badge de statut"""
        statut_classes = {
            'A_faire': 'bg-secondary',
            'En_cours': 'bg-primary',
            'En_pause': 'bg-warning',
            'Terminée': 'bg-success',
            'Bloquée': 'bg-danger',
            'Annulée': 'bg-dark',
        }
        return statut_classes.get(self.statut, 'bg-secondary')
    
    def get_priorite_badge_class(self):
        """Retourne la classe CSS pour le badge de priorité"""
        priorite_classes = {
            'Basse': 'bg-info',
            'Moyenne': 'bg-primary',
            'Haute': 'bg-warning',
            'Critique': 'bg-danger',
        }
        return priorite_classes.get(self.priorite, 'bg-secondary')
    
    def get_etat_reel(self):
        """Retourne l'état réel de la tâche"""
        if self.date_fin_reelle:
            return 'Terminée'
        elif self.is_en_retard() and self.statut != 'Terminée':
            return 'En retard'
        elif self.statut == 'En_cours':
            from datetime import date
            if self.date_debut <= date.today():
                return 'En cours'
        return 'Planifiée'
