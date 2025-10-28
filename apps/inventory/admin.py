from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UniteMessure, CategorieProduit, Produit, Stock,
    Achat, LigneAchat, MouvementStock
)


@admin.register(UniteMessure)
class UniteMessureAdmin(admin.ModelAdmin):
    list_display = ['nom', 'symbole', 'actif', 'date_creation']
    list_filter = ['actif']
    search_fields = ['nom', 'symbole']
    ordering = ['nom']


@admin.register(CategorieProduit)
class CategorieProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'actif', 'ordre_affichage', 'date_creation']
    list_filter = ['actif']
    search_fields = ['nom', 'code']
    ordering = ['ordre_affichage', 'nom']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['code_produit', 'nom', 'categorie', 'unite_mesure', 'prix_unitaire_moyen', 'stock_minimum', 'actif']
    list_filter = ['actif', 'categorie', 'unite_mesure']
    search_fields = ['code_produit', 'nom']
    readonly_fields = ['code_produit', 'date_creation', 'date_modification']
    ordering = ['nom']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code_produit', 'nom', 'categorie', 'unite_mesure', 'description')
        }),
        ('Gestion de stock', {
            'fields': ('prix_unitaire_moyen', 'stock_minimum', 'actif')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['produit', 'projet', 'quantite_actuelle', 'valeur_stock', 'emplacement', 'stock_status']
    list_filter = ['projet', 'produit__categorie']
    search_fields = ['produit__nom', 'projet__nom_projet', 'emplacement']
    readonly_fields = ['valeur_stock', 'date_creation', 'date_modification']
    ordering = ['projet', 'produit']
    
    def stock_status(self, obj):
        if obj.is_stock_faible():
            return format_html('<span style="color: red;">⚠️ Stock faible</span>')
        return format_html('<span style="color: green;">✓ Stock OK</span>')
    stock_status.short_description = 'Statut'


class LigneAchatInline(admin.TabularInline):
    model = LigneAchat
    extra = 1
    readonly_fields = ['montant_ligne']
    fields = ['produit', 'quantite', 'prix_unitaire', 'montant_ligne', 'notes']


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ['numero_achat', 'projet', 'fournisseur', 'date_achat', 'montant_total', 'statut', 'statut_badge']
    list_filter = ['statut', 'projet', 'fournisseur', 'date_achat']
    search_fields = ['numero_achat', 'numero_facture', 'fournisseur__nom']
    readonly_fields = ['numero_achat', 'montant_total', 'date_creation', 'date_modification']
    inlines = [LigneAchatInline]
    ordering = ['-date_achat']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero_achat', 'projet', 'fournisseur', 'date_achat', 'date_reception')
        }),
        ('Détails financiers', {
            'fields': ('numero_facture', 'montant_total', 'mode_paiement')
        }),
        ('Statut et validation', {
            'fields': ('statut', 'valide_par', 'date_validation', 'notes', 'piece_justificative')
        }),
        ('Informations système', {
            'fields': ('saisi_par', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def statut_badge(self, obj):
        colors = {
            'Brouillon': '#6c757d',
            'Validé': '#0dcaf0',
            'Reçu': '#198754',
            'Annulé': '#dc3545',
        }
        color = colors.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.statut
        )
    statut_badge.short_description = 'Statut'


@admin.register(LigneAchat)
class LigneAchatAdmin(admin.ModelAdmin):
    list_display = ['achat', 'produit', 'quantite', 'prix_unitaire', 'montant_ligne']
    list_filter = ['achat__projet', 'produit__categorie']
    search_fields = ['achat__numero_achat', 'produit__nom']
    readonly_fields = ['montant_ligne', 'date_creation']
    ordering = ['-date_creation']


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ['stock', 'type_mouvement', 'quantite', 'quantite_avant', 'quantite_apres', 'date_mouvement', 'effectue_par']
    list_filter = ['type_mouvement', 'stock__projet', 'date_mouvement']
    search_fields = ['stock__produit__nom', 'stock__projet__nom_projet', 'motif']
    readonly_fields = ['quantite_avant', 'quantite_apres', 'date_mouvement', 'date_creation']
    ordering = ['-date_mouvement']
    
    fieldsets = (
        ('Informations du mouvement', {
            'fields': ('stock', 'type_mouvement', 'quantite', 'quantite_avant', 'quantite_apres')
        }),
        ('Détails', {
            'fields': ('date_mouvement', 'achat', 'projet_destination', 'motif')
        }),
        ('Informations système', {
            'fields': ('effectue_par', 'date_creation'),
            'classes': ('collapse',)
        }),
    )
