from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Devis, Facture, LigneDevis, LigneFacture, PaiementFacture
from .forms import DevisForm, FactureForm, LigneDevisFormSet, LigneFactureFormSet, PaiementFactureForm


@login_required
def invoicing_home(request):
    """Page d'accueil du module facturation"""
    stats = {
        'total_devis': Devis.objects.count(),
        'devis_en_attente': Devis.objects.filter(statut='En attente').count(),
        'devis_acceptes': Devis.objects.filter(statut='Accepté').count(),
        'total_factures': Facture.objects.count(),
        'factures_impayees': Facture.objects.filter(statut_paiement='Impayée').count(),
        'montant_a_recevoir': Facture.objects.filter(statut_paiement__in=['Impayée', 'Partielle']).aggregate(
            total=Sum('montant_ht')
        )['total'] or 0,
    }
    
    devis_recents = Devis.objects.select_related('client', 'projet').order_by('-date_emission')[:5]
    factures_recentes = Facture.objects.select_related('client', 'projet').order_by('-date_emission')[:5]
    
    context = {
        'stats': stats,
        'devis_recents': devis_recents,
        'factures_recentes': factures_recentes,
    }
    return render(request, 'invoicing/home.html', context)


# ===== DEVIS =====
class DevisListView(LoginRequiredMixin, ListView):
    """Liste des devis"""
    model = Devis
    template_name = 'invoicing/devis_list.html'
    context_object_name = 'devis_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Devis.objects.select_related('client', 'projet').order_by('-date_emission')
        
        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_devis__icontains=search) |
                Q(client__nom_complet__icontains=search) |
                Q(projet__nom_projet__icontains=search)
            )
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculer les totaux pour la page actuelle
        devis_list = context['devis_list']
        context['total_ht'] = sum(d.montant_ht for d in devis_list)
        context['total_ttc'] = sum(d.montant_ttc for d in devis_list)
        return context


class DevisCreateView(LoginRequiredMixin, CreateView):
    """Création d'un devis"""
    model = Devis
    form_class = DevisForm
    template_name = 'invoicing/devis_form.html'
    success_url = reverse_lazy('invoicing:devis_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LigneDevisFormSet(self.request.POST)
        else:
            context['formset'] = LigneDevisFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        lignes = context['formset']
        
        self.object = form.save(commit=False)
        self.object.cree_par = self.request.user
        
        if lignes.is_valid():
            self.object.save()
            lignes.instance = self.object
            lignes.save()
            
            # Calculer le montant total
            self.object.calculer_montant_total()
            
            messages.success(self.request, f'Devis {self.object.numero_devis} créé avec succès.')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class DevisUpdateView(LoginRequiredMixin, UpdateView):
    """Modification d'un devis"""
    model = Devis
    form_class = DevisForm
    template_name = 'invoicing/devis_form.html'
    success_url = reverse_lazy('invoicing:devis_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LigneDevisFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = LigneDevisFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        lignes = context['formset']
        
        if lignes.is_valid():
            self.object = form.save()
            lignes.instance = self.object
            lignes.save()
            
            # Recalculer le montant total
            self.object.calculer_montant_total()
            
            messages.success(self.request, f'Devis {self.object.numero_devis} modifié avec succès.')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class DevisDetailView(LoginRequiredMixin, DetailView):
    """Détails d'un devis"""
    model = Devis
    template_name = 'invoicing/devis_detail.html'
    context_object_name = 'devis'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lignes'] = self.object.lignes.all()
        return context


# ===== FACTURES =====
class FactureListView(LoginRequiredMixin, ListView):
    """Liste des factures"""
    model = Facture
    template_name = 'invoicing/facture_list.html'
    context_object_name = 'factures'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Facture.objects.select_related('client', 'projet', 'devis').order_by('-date_emission')
        
        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_facture__icontains=search) |
                Q(client__nom_complet__icontains=search) |
                Q(projet__nom_projet__icontains=search)
            )
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut_paiement=statut)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculer les totaux pour la page actuelle
        factures = context['factures']
        context['total_ht'] = sum(f.montant_ht for f in factures)
        context['total_ttc'] = sum(f.montant_ttc for f in factures)
        context['total_paye'] = sum(f.montant_paye for f in factures)
        context['total_restant'] = sum(f.montant_restant for f in factures)
        return context


class FactureCreateView(LoginRequiredMixin, CreateView):
    """Création d'une facture"""
    model = Facture
    form_class = FactureForm
    template_name = 'invoicing/facture_form.html'
    success_url = reverse_lazy('invoicing:facture_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LigneFactureFormSet(self.request.POST)
        else:
            context['formset'] = LigneFactureFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        lignes = context['formset']
        
        self.object = form.save(commit=False)
        self.object.cree_par = self.request.user
        
        if lignes.is_valid():
            self.object.save()
            lignes.instance = self.object
            lignes.save()
            
            # Calculer le montant total
            self.object.calculer_montant_total()
            
            messages.success(self.request, f'Facture {self.object.numero_facture} créée avec succès.')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class FactureUpdateView(LoginRequiredMixin, UpdateView):
    """Modification d'une facture"""
    model = Facture
    form_class = FactureForm
    template_name = 'invoicing/facture_form.html'
    success_url = reverse_lazy('invoicing:facture_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = LigneFactureFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = LigneFactureFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        lignes = context['formset']
        
        if lignes.is_valid():
            self.object = form.save()
            lignes.instance = self.object
            lignes.save()
            
            # Recalculer le montant total
            self.object.calculer_montant_total()
            
            messages.success(self.request, f'Facture {self.object.numero_facture} modifiée avec succès.')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class FactureDetailView(LoginRequiredMixin, DetailView):
    """Détails d'une facture"""
    model = Facture
    template_name = 'invoicing/facture_detail.html'
    context_object_name = 'facture'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lignes'] = self.object.lignes.all()
        context['paiements'] = self.object.paiements.all().order_by('-date_paiement')
        return context


@login_required
def ajouter_paiement(request, pk):
    """Ajouter un paiement à une facture"""
    facture = get_object_or_404(Facture, pk=pk)
    
    if request.method == 'POST':
        form = PaiementFactureForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.facture = facture
            paiement.enregistre_par = request.user
            paiement.save()
            
            # Mettre à jour le statut de la facture
            facture.mettre_a_jour_statut_paiement()
            
            messages.success(request, 'Paiement enregistré avec succès.')
            return redirect('invoicing:facture_detail', pk=facture.pk)
    else:
        form = PaiementFactureForm()
    
    context = {
        'form': form,
        'facture': facture,
    }
    return render(request, 'invoicing/paiement_form.html', context)
