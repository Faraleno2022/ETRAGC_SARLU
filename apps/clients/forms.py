from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    """Formulaire pour les clients"""
    
    class Meta:
        model = Client
        fields = ['nom_complet', 'entreprise', 'telephone', 'telephone_2', 
                  'email', 'adresse', 'ville', 'pays', 'nif', 'rccm', 'notes', 'actif']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone_2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'nif': forms.TextInput(attrs={'class': 'form-control'}),
            'rccm': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
