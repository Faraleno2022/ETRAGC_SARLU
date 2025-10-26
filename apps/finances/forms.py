from django import forms
from .models import Transaction, Depense, CategorieDepense, Fournisseur


class TransactionForm(forms.ModelForm):
    """Formulaire pour les transactions"""
    
    class Meta:
        model = Transaction
        fields = ['projet', 'type', 'montant', 'date_transaction', 'reference',
                  'mode_paiement', 'description', 'piece_justificative']
        widgets = {
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.TextInput(attrs={'class': 'form-control money-input', 'inputmode': 'decimal'}),
            'date_transaction': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'piece_justificative': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DepenseForm(forms.ModelForm):
    """Formulaire pour les dépenses"""
    
    class Meta:
        model = Depense
        fields = ['projet', 'categorie', 'fournisseur', 'date_depense', 'montant',
                  'mode_paiement', 'numero_facture', 'description', 'piece_justificative']
        widgets = {
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'fournisseur': forms.Select(attrs={'class': 'form-select'}),
            'date_depense': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant': forms.TextInput(attrs={'class': 'form-control money-input', 'inputmode': 'decimal'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'numero_facture': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'piece_justificative': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CategorieDepenseForm(forms.ModelForm):
    """Formulaire pour les catégories de dépenses"""
    
    class Meta:
        model = CategorieDepense
        fields = ['nom', 'code', 'couleur_hex', 'description', 'actif', 'ordre_affichage']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'couleur_hex': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ordre_affichage': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FournisseurForm(forms.ModelForm):
    """Formulaire pour les fournisseurs"""
    
    class Meta:
        model = Fournisseur
        fields = ['nom', 'contact', 'telephone', 'telephone_2', 'email', 
                  'adresse', 'ville', 'nif', 'type', 'notes', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone_2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'nif': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
