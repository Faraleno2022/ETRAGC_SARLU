from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Transaction, Depense, CategorieDepense, Fournisseur
from .forms import TransactionForm, DepenseForm, CategorieDepenseForm, FournisseurForm


# Transaction Views
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finances/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transaction.objects.select_related('projet', 'saisi_par').all()
        search = self.request.GET.get('search')
        type_filter = self.request.GET.get('type')
        
        if search:
            queryset = queryset.filter(
                Q(projet__code_projet__icontains=search) |
                Q(reference__icontains=search)
            )
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        
        return queryset


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:transaction_list')
    
    def form_valid(self, form):
        form.instance.saisi_par = self.request.user
        messages.success(self.request, 'Transaction enregistrée avec succès.')
        return super().form_valid(form)


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'finances/transaction_detail.html'
    context_object_name = 'transaction'


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """Suppression d'une transaction"""
    model = Transaction
    template_name = 'finances/transaction_confirm_delete.html'
    success_url = reverse_lazy('finances:transaction_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Transaction supprimée avec succès.')
        return super().delete(request, *args, **kwargs)


# Depense Views
class DepenseListView(LoginRequiredMixin, ListView):
    model = Depense
    template_name = 'finances/depense_list.html'
    context_object_name = 'depenses'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Depense.objects.select_related('projet', 'categorie', 'fournisseur').all()
        search = self.request.GET.get('search')
        statut = self.request.GET.get('statut')
        
        if search:
            queryset = queryset.filter(
                Q(projet__code_projet__icontains=search) |
                Q(description__icontains=search)
            )
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset


class DepenseCreateView(LoginRequiredMixin, CreateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'finances/depense_form.html'
    success_url = reverse_lazy('finances:depense_list')
    
    def form_valid(self, form):
        form.instance.saisi_par = self.request.user
        messages.success(self.request, 'Dépense enregistrée avec succès.')
        return super().form_valid(form)


class DepenseDetailView(LoginRequiredMixin, DetailView):
    model = Depense
    template_name = 'finances/depense_detail.html'
    context_object_name = 'depense'


class DepenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'finances/depense_form.html'
    success_url = reverse_lazy('finances:depense_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Dépense mise à jour avec succès.')
        return super().form_valid(form)


@login_required
def depense_valider(request, pk):
    """Valider une dépense"""
    if not request.user.can_validate_expenses():
        messages.error(request, 'Vous n\'avez pas la permission de valider les dépenses.')
        return redirect('finances:depense_list')
    
    depense = get_object_or_404(Depense, pk=pk)
    depense.statut = 'Validée'
    depense.date_validation = timezone.now()
    depense.validee_par = request.user
    depense.save()
    
    messages.success(request, 'Dépense validée avec succès.')
    return redirect('finances:depense_detail', pk=pk)


@login_required
def depense_rejeter(request, pk):
    """Rejeter une dépense"""
    if not request.user.can_validate_expenses():
        messages.error(request, 'Vous n\'avez pas la permission de rejeter les dépenses.')
        return redirect('finances:depense_list')
    
    depense = get_object_or_404(Depense, pk=pk)
    depense.statut = 'Rejetée'
    depense.save()
    
    messages.warning(request, 'Dépense rejetée.')
    return redirect('finances:depense_detail', pk=pk)


# Fournisseur Views
class FournisseurListView(LoginRequiredMixin, ListView):
    model = Fournisseur
    template_name = 'finances/fournisseur_list.html'
    context_object_name = 'fournisseurs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Fournisseur.objects.all()
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) |
                Q(contact__icontains=search)
            )
        
        return queryset


class FournisseurCreateView(LoginRequiredMixin, CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'finances/fournisseur_form.html'
    success_url = reverse_lazy('finances:fournisseur_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fournisseur créé avec succès.')
        return super().form_valid(form)


class FournisseurDetailView(LoginRequiredMixin, DetailView):
    model = Fournisseur
    template_name = 'finances/fournisseur_detail.html'
    context_object_name = 'fournisseur'


class FournisseurUpdateView(LoginRequiredMixin, UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = 'finances/fournisseur_form.html'
    success_url = reverse_lazy('finances:fournisseur_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fournisseur mis à jour avec succès.')
        return super().form_valid(form)


# Categorie Depense Views
class CategorieDepenseListView(LoginRequiredMixin, ListView):
    model = CategorieDepense
    template_name = 'finances/categorie_list.html'
    context_object_name = 'categories'


class CategorieDepenseCreateView(LoginRequiredMixin, CreateView):
    model = CategorieDepense
    form_class = CategorieDepenseForm
    template_name = 'finances/categorie_form.html'
    success_url = reverse_lazy('finances:categorie_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Catégorie créée avec succès.')
        return super().form_valid(form)
