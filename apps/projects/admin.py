from django.contrib import admin
from .models import Projet


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['code_projet', 'nom_projet', 'client', 'responsable', 'statut', 'montant_prevu', 'pourcentage_avancement', 'date_debut']
    list_filter = ['statut', 'date_debut', 'date_creation']
    search_fields = ['code_projet', 'nom_projet', 'client__nom_complet', 'adresse_chantier']
    readonly_fields = ['code_projet', 'date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('code_projet', 'nom_projet', 'client', 'responsable', 'statut')
        }),
        ('Budget', {
            'fields': ('montant_prevu',)
        }),
        ('Planning', {
            'fields': ('date_debut', 'date_fin_prevue', 'date_fin_reelle', 'pourcentage_avancement')
        }),
        ('Localisation', {
            'fields': ('adresse_chantier', 'ville_chantier')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
