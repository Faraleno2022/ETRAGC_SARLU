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
        from django.db.models import Sum, Count
        from django.db.models.functions import TruncDate
        
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
        context['depenses_recentes'] = projet.depenses.filter(statut='Validée').select_related('categorie', 'fournisseur')[:10]
        
        # Dépenses groupées par date
        context['depenses_par_date'] = projet.depenses.filter(
            statut='Validée'
        ).values('date_depense').annotate(
            total=Sum('montant'),
            nombre=Count('id')
        ).order_by('-date_depense')[:20]
        
        # Factures du projet
        context['factures'] = projet.factures.select_related('client', 'devis').order_by('-date_emission')[:10]
        context['total_factures'] = projet.factures.aggregate(total=Sum('montant_ht'))['total'] or 0
        
        # Paiements du personnel
        context['paiements_personnel'] = projet.paiements_personnel.filter(
            statut='Validé'
        ).select_related('personnel', 'saisi_par').order_by('-date_paiement')[:10]
        context['total_paiements_personnel'] = projet.paiements_personnel.filter(
            statut='Validé'
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        # Personnel affecté au projet
        context['personnel_affecte'] = projet.affectations_personnel.filter(
            date_fin__isnull=True
        ).select_related('personnel')
        
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projet = self.object
        
        # Compter les éléments liés qui seront supprimés
        context['nb_taches'] = projet.taches.count()
        context['nb_transactions'] = projet.transactions.count()
        context['nb_depenses'] = projet.depenses.count()
        context['nb_factures'] = projet.factures.count()
        context['nb_devis'] = projet.devis.count()
        context['nb_affectations'] = projet.affectations_personnel.count()
        context['nb_paiements_personnel'] = projet.paiements_personnel.count()
        
        # Total des éléments
        context['total_elements'] = (
            context['nb_taches'] + 
            context['nb_transactions'] + 
            context['nb_depenses'] + 
            context['nb_factures'] + 
            context['nb_devis'] + 
            context['nb_affectations'] + 
            context['nb_paiements_personnel']
        )
        
        return context
    
    def delete(self, request, *args, **kwargs):
        projet_nom = self.get_object().nom_projet
        messages.warning(request, f'Projet "{projet_nom}" et toutes ses données associées ont été supprimés.')
        return super().delete(request, *args, **kwargs)
