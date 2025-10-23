from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour ETRAGC
    """
    ROLE_CHOICES = [
        ('Admin', 'Administrateur'),
        ('Manager', 'Manager de Projet'),
        ('Comptable', 'Comptable'),
        ('Chef_Chantier', 'Chef de Chantier'),
        ('Lecteur', 'Lecteur'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Lecteur',
        verbose_name='Rôle'
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Téléphone'
    )
    photo_profil = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        verbose_name='Photo de profil'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    derniere_connexion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Dernière connexion'
    )
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username
    
    def has_role(self, role):
        """Vérifie si l'utilisateur a un rôle spécifique"""
        return self.role == role
    
    def is_admin(self):
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == 'Admin' or self.is_superuser
    
    def is_manager(self):
        """Vérifie si l'utilisateur est manager"""
        return self.role in ['Admin', 'Manager']
    
    def is_comptable(self):
        """Vérifie si l'utilisateur est comptable"""
        return self.role in ['Admin', 'Comptable']
    
    def can_edit_finances(self):
        """Vérifie si l'utilisateur peut éditer les finances"""
        return self.role in ['Admin', 'Manager', 'Comptable']
    
    def can_validate_expenses(self):
        """Vérifie si l'utilisateur peut valider les dépenses"""
        return self.role in ['Admin', 'Comptable']
