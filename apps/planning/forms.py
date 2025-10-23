from django import forms
from .models import Tache


class TacheForm(forms.ModelForm):
    """Formulaire pour les tâches"""
    class Meta:
        model = Tache
        fields = [
            'projet', 'nom_tache', 'description', 'date_debut', 'date_fin_prevue',
            'date_fin_reelle', 'priorite', 'statut', 'pourcentage_progression',
            'responsable', 'tache_parent', 'ordre_affichage'
        ]
        widgets = {
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'nom_tache': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_reelle': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priorite': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'pourcentage_progression': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'tache_parent': forms.Select(attrs={'class': 'form-select'}),
            'ordre_affichage': forms.NumberInput(attrs={'class': 'form-control'}),
        }
