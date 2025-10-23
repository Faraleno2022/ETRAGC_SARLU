from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'actif', 'is_staff']
    list_filter = ['role', 'actif', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations ETRAGC', {
            'fields': ('role', 'telephone', 'photo_profil', 'actif', 'derniere_connexion')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations ETRAGC', {
            'fields': ('role', 'telephone', 'actif')
        }),
    )
