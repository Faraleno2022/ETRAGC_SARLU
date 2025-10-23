from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Document(models.Model):
    """
    Modèle pour gérer les documents et fichiers des projets
    """
    TYPE_DOCUMENT_CHOICES = [
        ('Photo', 'Photo'),
        ('Plan', 'Plan'),
        ('Contrat', 'Contrat'),
        ('Rapport', 'Rapport'),
        ('Facture_Fournisseur', 'Facture Fournisseur'),
        ('Autre', 'Autre'),
    ]
    
    projet = models.ForeignKey(
        'projects.Projet',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name='Projet'
    )
    type_document = models.CharField(
        max_length=30,
        choices=TYPE_DOCUMENT_CHOICES,
        verbose_name='Type de document'
    )
    nom_fichier = models.CharField(
        max_length=255,
        verbose_name='Nom du fichier'
    )
    fichier = models.FileField(
        upload_to='documents/%Y/%m/',
        verbose_name='Fichier'
    )
    taille_ko = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Taille (Ko)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    upload_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='documents_uploades',
        verbose_name='Uploadé par'
    )
    date_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'upload'
    )
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-date_upload']
        indexes = [
            models.Index(fields=['projet']),
            models.Index(fields=['type_document']),
        ]
    
    def __str__(self):
        return self.nom_fichier
    
    def save(self, *args, **kwargs):
        if self.fichier:
            # Calculer la taille en Ko
            self.taille_ko = self.fichier.size // 1024
        super().save(*args, **kwargs)
    
    def get_taille_formatee(self):
        """Retourne la taille formatée"""
        if self.taille_ko:
            if self.taille_ko < 1024:
                return f"{self.taille_ko} Ko"
            else:
                return f"{self.taille_ko / 1024:.2f} Mo"
        return "N/A"


class Parametre(models.Model):
    """
    Modèle pour stocker les paramètres de configuration de l'application
    """
    TYPE_DONNEE_CHOICES = [
        ('Texte', 'Texte'),
        ('Nombre', 'Nombre'),
        ('Boolean', 'Boolean'),
        ('JSON', 'JSON'),
    ]
    
    cle = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Clé'
    )
    valeur = models.TextField(
        blank=True,
        null=True,
        verbose_name='Valeur'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description'
    )
    type_donnee = models.CharField(
        max_length=20,
        choices=TYPE_DONNEE_CHOICES,
        default='Texte',
        verbose_name='Type de donnée'
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    class Meta:
        verbose_name = 'Paramètre'
        verbose_name_plural = 'Paramètres'
        ordering = ['cle']
    
    def __str__(self):
        return f"{self.cle}: {self.valeur}"
    
    @classmethod
    def get_valeur(cls, cle, defaut=None):
        """Récupère la valeur d'un paramètre"""
        try:
            param = cls.objects.get(cle=cle)
            if param.type_donnee == 'Nombre':
                return float(param.valeur) if param.valeur else defaut
            elif param.type_donnee == 'Boolean':
                return param.valeur.lower() in ['true', '1', 'oui'] if param.valeur else defaut
            elif param.type_donnee == 'JSON':
                import json
                return json.loads(param.valeur) if param.valeur else defaut
            return param.valeur if param.valeur else defaut
        except cls.DoesNotExist:
            return defaut
    
    @classmethod
    def set_valeur(cls, cle, valeur, description=None, type_donnee='Texte'):
        """Définit la valeur d'un paramètre"""
        param, created = cls.objects.get_or_create(
            cle=cle,
            defaults={
                'valeur': str(valeur),
                'description': description,
                'type_donnee': type_donnee
            }
        )
        if not created:
            param.valeur = str(valeur)
            if description:
                param.description = description
            param.type_donnee = type_donnee
            param.save()
        return param


class HistoriqueModification(models.Model):
    """
    Modèle pour tracer les modifications importantes (audit trail)
    """
    TYPE_ACTION_CHOICES = [
        ('Création', 'Création'),
        ('Modification', 'Modification'),
        ('Suppression', 'Suppression'),
    ]
    
    table_concernee = models.CharField(
        max_length=50,
        verbose_name='Table concernée'
    )
    id_enregistrement = models.IntegerField(
        verbose_name='ID enregistrement'
    )
    type_action = models.CharField(
        max_length=20,
        choices=TYPE_ACTION_CHOICES,
        verbose_name='Type d\'action'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='modifications_effectuees',
        verbose_name='Utilisateur'
    )
    anciennes_valeurs = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Anciennes valeurs'
    )
    nouvelles_valeurs = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Nouvelles valeurs'
    )
    date_action = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de l\'action'
    )
    
    class Meta:
        verbose_name = 'Historique de modification'
        verbose_name_plural = 'Historiques de modifications'
        ordering = ['-date_action']
        indexes = [
            models.Index(fields=['table_concernee']),
            models.Index(fields=['date_action']),
            models.Index(fields=['utilisateur']),
        ]
    
    def __str__(self):
        return f"{self.type_action} - {self.table_concernee} #{self.id_enregistrement}"


class Notification(models.Model):
    """
    Modèle pour gérer les notifications internes
    """
    TYPE_CHOICES = [
        ('Info', 'Info'),
        ('Alerte', 'Alerte'),
        ('Erreur', 'Erreur'),
        ('Succès', 'Succès'),
    ]
    
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Utilisateur'
    )
    titre = models.CharField(
        max_length=255,
        verbose_name='Titre'
    )
    message = models.TextField(
        verbose_name='Message'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='Info',
        verbose_name='Type'
    )
    lu = models.BooleanField(
        default=False,
        verbose_name='Lu'
    )
    lien = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Lien'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    date_lecture = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de lecture'
    )
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur']),
            models.Index(fields=['lu']),
            models.Index(fields=['date_creation']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur.username}"
    
    def marquer_comme_lu(self):
        """Marque la notification comme lue"""
        if not self.lu:
            from django.utils import timezone
            self.lu = True
            self.date_lecture = timezone.now()
            self.save()
    
    def get_type_badge_class(self):
        """Retourne la classe CSS pour le badge de type"""
        type_classes = {
            'Info': 'bg-info',
            'Alerte': 'bg-warning',
            'Erreur': 'bg-danger',
            'Succès': 'bg-success',
        }
        return type_classes.get(self.type, 'bg-secondary')
