from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'entreprise', 'telephone', 'email', 'ville', 'actif', 'date_creation']
    list_filter = ['actif', 'ville', 'pays', 'date_creation']
    search_fields = ['nom_complet', 'entreprise', 'email', 'telephone', 'nif', 'rccm']
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom_complet', 'entreprise', 'actif')
        }),
        ('Contact', {
            'fields': ('telephone', 'telephone_2', 'email')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'pays')
        }),
        ('Informations légales', {
            'fields': ('nif', 'rccm')
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
