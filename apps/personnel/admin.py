from django.contrib import admin
from .models import Personnel, AffectationPersonnel, PaiementPersonnel


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'fonction', 'type_contrat', 'actif', 'date_embauche']
    list_filter = ['fonction', 'type_contrat', 'actif']
    search_fields = ['nom', 'prenom', 'telephone', 'email']
    ordering = ['nom', 'prenom']


@admin.register(AffectationPersonnel)
class AffectationPersonnelAdmin(admin.ModelAdmin):
    list_display = ['personnel', 'projet', 'role_chantier', 'date_debut', 'date_fin']
    list_filter = ['role_chantier', 'date_debut']
    search_fields = ['personnel__nom', 'personnel__prenom', 'projet__code_projet', 'projet__nom_projet']
    raw_id_fields = ['personnel', 'projet']
    date_hierarchy = 'date_debut'


@admin.register(PaiementPersonnel)
class PaiementPersonnelAdmin(admin.ModelAdmin):
    list_display = ['personnel', 'projet', 'date_paiement', 'montant', 'mode_paiement', 'statut', 'saisi_par']
    list_filter = ['statut', 'mode_paiement', 'date_paiement']
    search_fields = ['personnel__nom', 'personnel__prenom', 'projet__code_projet', 'description']
    raw_id_fields = ['personnel', 'projet', 'saisi_par', 'valide_par']
    date_hierarchy = 'date_paiement'
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('personnel', 'projet', 'date_paiement', 'montant', 'nombre_jours')
        }),
        ('Paiement', {
            'fields': ('mode_paiement', 'statut', 'description', 'piece_justificative')
        }),
        ('Validation', {
            'fields': ('saisi_par', 'date_validation', 'valide_par')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
