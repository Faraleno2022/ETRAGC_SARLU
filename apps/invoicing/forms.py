from django import forms
from django.forms import inlineformset_factory
from .models import Devis, Facture, LigneDevis, LigneFacture, PaiementFacture


class DevisForm(forms.ModelForm):
    """Formulaire pour les devis"""
    class Meta:
        model = Devis
        fields = ['client', 'projet', 'date_emission', 'date_validite', 'conditions_paiement', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'date_emission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_validite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conditions_paiement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LigneDevisForm(forms.ModelForm):
    """Formulaire pour les lignes de devis"""
    class Meta:
        model = LigneDevis
        fields = ['description', 'quantite', 'prix_unitaire_ht']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qté', 'step': '0.01'}),
            'prix_unitaire_ht': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix unitaire', 'step': '0.01'}),
        }


LigneDevisFormSet = inlineformset_factory(
    Devis,
    LigneDevis,
    form=LigneDevisForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class FactureForm(forms.ModelForm):
    """Formulaire pour les factures"""
    class Meta:
        model = Facture
        fields = ['client', 'projet', 'devis', 'date_emission', 'date_echeance', 'conditions_paiement', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'devis': forms.Select(attrs={'class': 'form-select'}),
            'date_emission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conditions_paiement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LigneFactureForm(forms.ModelForm):
    """Formulaire pour les lignes de facture"""
    class Meta:
        model = LigneFacture
        fields = ['description', 'quantite', 'prix_unitaire_ht']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qté', 'step': '0.01'}),
            'prix_unitaire_ht': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix unitaire', 'step': '0.01'}),
        }


LigneFactureFormSet = inlineformset_factory(
    Facture,
    LigneFacture,
    form=LigneFactureForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class PaiementFactureForm(forms.ModelForm):
    """Formulaire pour les paiements de facture"""
    class Meta:
        model = PaiementFacture
        fields = ['montant', 'date_paiement', 'mode_paiement', 'reference', 'notes']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_paiement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
