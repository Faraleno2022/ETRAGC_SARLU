from django.contrib import admin
from .models import Transaction, CategorieDepense, Fournisseur, Depense


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['projet', 'type', 'montant', 'date_transaction', 'mode_paiement', 'saisi_par', 'date_creation']
    list_filter = ['type', 'mode_paiement', 'date_transaction', 'date_creation']
    search_fields = ['projet__code_projet', 'projet__nom_projet', 'reference', 'description']
    readonly_fields = ['date_creation']
    date_hierarchy = 'date_transaction'
    
    fieldsets = (
        ('Transaction', {
            'fields': ('projet', 'type', 'montant', 'date_transaction')
        }),
        ('Paiement', {
            'fields': ('mode_paiement', 'reference')
        }),
        ('Détails', {
            'fields': ('description', 'piece_justificative', 'saisi_par')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )


@admin.register(CategorieDepense)
class CategorieDepenseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'couleur_hex', 'ordre_affichage', 'actif', 'date_creation']
    list_filter = ['actif', 'date_creation']
    search_fields = ['nom', 'code', 'description']
    readonly_fields = ['date_creation']
    ordering = ['ordre_affichage', 'nom']


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'contact', 'telephone', 'email', 'type', 'ville', 'actif', 'date_creation']
    list_filter = ['type', 'actif', 'ville', 'date_creation']
    search_fields = ['nom', 'contact', 'telephone', 'email', 'nif']
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'type', 'actif')
        }),
        ('Contact', {
            'fields': ('contact', 'telephone', 'telephone_2', 'email')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville')
        }),
        ('Informations légales', {
            'fields': ('nif',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ['projet', 'categorie', 'fournisseur', 'montant', 'date_depense', 'statut', 'saisi_par', 'date_creation']
    list_filter = ['statut', 'categorie', 'mode_paiement', 'date_depense', 'date_creation']
    search_fields = ['projet__code_projet', 'projet__nom_projet', 'fournisseur__nom', 'numero_facture', 'description']
    readonly_fields = ['date_creation', 'date_modification']
    date_hierarchy = 'date_depense'
    
    fieldsets = (
        ('Dépense', {
            'fields': ('projet', 'categorie', 'fournisseur', 'montant', 'date_depense')
        }),
        ('Paiement', {
            'fields': ('mode_paiement', 'numero_facture')
        }),
        ('Détails', {
            'fields': ('description', 'piece_justificative')
        }),
        ('Validation', {
            'fields': ('statut', 'saisi_par', 'validee_par', 'date_validation')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
