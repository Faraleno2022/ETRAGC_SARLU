from django import forms
from .models import Projet


class ProjetForm(forms.ModelForm):
    """Formulaire pour les projets"""
    
    class Meta:
        model = Projet
        fields = ['nom_projet', 'client', 'responsable', 'montant_prevu', 
                  'date_debut', 'date_fin_prevue', 'date_fin_reelle', 'statut',
                  'description', 'adresse_chantier', 'ville_chantier', 'pourcentage_avancement']
        widgets = {
            'nom_projet': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'montant_prevu': forms.TextInput(attrs={'class': 'form-control money-input', 'inputmode': 'decimal'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_reelle': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'adresse_chantier': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ville_chantier': forms.TextInput(attrs={'class': 'form-control'}),
            'pourcentage_avancement': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }
