from django import forms
from .models import Personnel, AffectationPersonnel


class PersonnelForm(forms.ModelForm):
    """Formulaire pour le personnel"""
    class Meta:
        model = Personnel
        fields = [
            'nom', 'prenom', 'telephone', 'telephone_2', 'email', 'adresse',
            'fonction', 'type_contrat', 'salaire_journalier', 'date_embauche',
            'date_fin_contrat', 'photo', 'actif', 'notes'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone_2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fonction': forms.Select(attrs={'class': 'form-select'}),
            'type_contrat': forms.Select(attrs={'class': 'form-select'}),
            'salaire_journalier': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_contrat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AffectationPersonnelForm(forms.ModelForm):
    """Formulaire pour les affectations"""
    class Meta:
        model = AffectationPersonnel
        fields = ['personnel', 'projet', 'role_chantier', 'date_debut', 'date_fin', 'notes']
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-select'}),
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'role_chantier': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
