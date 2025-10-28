from django import forms
from django.forms import inlineformset_factory
from .models import (
    UniteMessure, CategorieProduit, Produit, Stock,
    Achat, LigneAchat, MouvementStock
)


class UniteMessureForm(forms.ModelForm):
    class Meta:
        model = UniteMessure
        fields = ['nom', 'symbole', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'symbole': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategorieProduitForm(forms.ModelForm):
    class Meta:
        model = CategorieProduit
        fields = ['nom', 'code', 'description', 'ordre_affichage', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ordre_affichage': forms.NumberInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'categorie', 'unite_mesure', 'description', 'prix_unitaire_moyen', 'stock_minimum', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'unite_mesure': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prix_unitaire_moyen': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimum': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['projet', 'produit', 'quantite_actuelle', 'emplacement']
        widgets = {
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'quantite_actuelle': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'emplacement': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['projet', 'fournisseur', 'date_achat', 'date_reception', 'numero_facture', 
                  'mode_paiement', 'statut', 'notes', 'piece_justificative']
        widgets = {
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'fournisseur': forms.Select(attrs={'class': 'form-select'}),
            'date_achat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_reception': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numero_facture': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'piece_justificative': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LigneAchatForm(forms.ModelForm):
    class Meta:
        model = LigneAchat
        fields = ['produit', 'quantite', 'prix_unitaire', 'notes']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# Formset pour les lignes d'achat
LigneAchatFormSet = inlineformset_factory(
    Achat,
    LigneAchat,
    form=LigneAchatForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class MouvementStockForm(forms.ModelForm):
    class Meta:
        model = MouvementStock
        fields = ['stock', 'type_mouvement', 'quantite', 'projet_destination', 'motif']
        widgets = {
            'stock': forms.Select(attrs={'class': 'form-select'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'projet_destination': forms.Select(attrs={'class': 'form-select'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le projet destination obligatoire uniquement pour les transferts
        self.fields['projet_destination'].required = False


class StockFilterForm(forms.Form):
    """Formulaire pour filtrer les stocks"""
    projet = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Tous les projets',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    categorie = forms.ModelChoiceField(
        queryset=CategorieProduit.objects.filter(actif=True),
        required=False,
        empty_label='Toutes les catégories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    stock_faible = forms.BooleanField(
        required=False,
        label='Afficher uniquement les stocks faibles',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.projects.models import Projet
        self.fields['projet'].queryset = Projet.objects.filter(statut__in=['Planifié', 'En_cours'])


class AchatFilterForm(forms.Form):
    """Formulaire pour filtrer les achats"""
    projet = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Tous les projets',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fournisseur = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Tous les fournisseurs',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Achat.STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.projects.models import Projet
        from apps.finances.models import Fournisseur
        self.fields['projet'].queryset = Projet.objects.all()
        self.fields['fournisseur'].queryset = Fournisseur.objects.filter(actif=True)
