from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Projet
from .forms import ProjetForm


class ProjetListView(LoginRequiredMixin, ListView):
    """Liste des projets"""
    model = Projet
    template_name = 'projects/projet_list.html'
    context_object_name = 'projets'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Projet.objects.select_related('client', 'responsable').all()
        
        # Filtres
        search = self.request.GET.get('search')
        statut = self.request.GET.get('statut')
        
        if search:
            queryset = queryset.filter(
                Q(code_projet__icontains=search) |
                Q(nom_projet__icontains=search) |
                Q(client__nom_complet__icontains=search)
            )
        
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuts'] = Projet.STATUT_CHOICES
        return context


class ProjetDetailView(LoginRequiredMixin, DetailView):
    """Détails d'un projet"""
    model = Projet
    template_name = 'projects/projet_detail.html'
    context_object_name = 'projet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projet = self.object
        
        # Statistiques financières
        context['total_depots'] = projet.get_total_depots()
        context['total_retraits'] = projet.get_total_retraits()
        context['solde_disponible'] = projet.get_solde_disponible()
        context['total_depenses'] = projet.get_total_depenses()
        context['pourcentage_budget_consomme'] = projet.get_pourcentage_budget_consomme()
        
        # Transactions et dépenses récentes
        context['transactions_recentes'] = projet.transactions.all()[:10]
        context['depenses_recentes'] = projet.depenses.all()[:10]
        
        return context


class ProjetCreateView(LoginRequiredMixin, CreateView):
    """Création d'un projet"""
    model = Projet
    form_class = ProjetForm
    template_name = 'projects/projet_form.html'
    success_url = reverse_lazy('projects:list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Projet "{form.instance.nom_projet}" créé avec succès.')
        return super().form_valid(form)


class ProjetUpdateView(LoginRequiredMixin, UpdateView):
    """Mise à jour d'un projet"""
    model = Projet
    form_class = ProjetForm
    template_name = 'projects/projet_form.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Projet mis à jour avec succès.')
        return super().form_valid(form)


class ProjetDeleteView(LoginRequiredMixin, DeleteView):
    """Suppression d'un projet"""
    model = Projet
    template_name = 'projects/projet_confirm_delete.html'
    success_url = reverse_lazy('projects:list')
    
    def delete(self, request, *args, **kwargs):
        messages.warning(request, 'Projet supprimé.')
        return super().delete(request, *args, **kwargs)
