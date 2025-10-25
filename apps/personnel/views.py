from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from .models import Personnel, AffectationPersonnel, PaiementPersonnel
from .forms import PersonnelForm, AffectationPersonnelForm, PaiementPersonnelForm


@login_required
def personnel_home(request):
    """Page d'accueil du module personnel"""
    from django.db.models import Sum
    
    stats = {
        'total_personnel': Personnel.objects.count(),
        'personnel_actif': Personnel.objects.filter(actif=True).count(),
        'personnel_inactif': Personnel.objects.filter(actif=False).count(),
        'total_affectations': AffectationPersonnel.objects.filter(date_fin__isnull=True).count(),
        'total_paiements': PaiementPersonnel.objects.count(),
        'paiements_en_attente': PaiementPersonnel.objects.filter(statut='En_attente').count(),
        'paiements_valides': PaiementPersonnel.objects.filter(statut='Validé').count(),
        'montant_total_paye': PaiementPersonnel.objects.filter(statut='Validé').aggregate(
            total=Sum('montant')
        )['total'] or 0,
    }
    
    personnel_recents = Personnel.objects.order_by('-date_embauche')[:5]
    affectations_actives = AffectationPersonnel.objects.filter(
        date_fin__isnull=True
    ).select_related('personnel', 'projet')[:5]
    paiements_recents = PaiementPersonnel.objects.select_related(
        'personnel', 'projet'
    ).order_by('-date_paiement')[:5]
    
    context = {
        'stats': stats,
        'personnel_recents': personnel_recents,
        'affectations_actives': affectations_actives,
        'paiements_recents': paiements_recents,
    }
    return render(request, 'personnel/home.html', context)


# ===== PERSONNEL =====
class PersonnelListView(LoginRequiredMixin, ListView):
    """Liste des employés"""
    model = Personnel
    template_name = 'personnel/employe_list.html'
    context_object_name = 'employes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Personnel.objects.all().order_by('nom', 'prenom')
        
        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) |
                Q(prenom__icontains=search) |
                Q(matricule__icontains=search) |
                Q(telephone__icontains=search)
            )
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut == 'actif':
            queryset = queryset.filter(actif=True)
        elif statut == 'inactif':
            queryset = queryset.filter(actif=False)
        
        # Filtre par fonction
        fonction = self.request.GET.get('fonction')
        if fonction:
            queryset = queryset.filter(fonction=fonction)
        
        return queryset


class PersonnelCreateView(LoginRequiredMixin, CreateView):
    """Création d'un employé"""
    model = Personnel
    form_class = PersonnelForm
    template_name = 'personnel/employe_form.html'
    success_url = reverse_lazy('personnel:employe_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Employé {form.instance.get_full_name()} créé avec succès.')
        return super().form_valid(form)


class PersonnelUpdateView(LoginRequiredMixin, UpdateView):
    """Modification d'un employé"""
    model = Personnel
    form_class = PersonnelForm
    template_name = 'personnel/employe_form.html'
    success_url = reverse_lazy('personnel:employe_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Employé {form.instance.get_full_name()} modifié avec succès.')
        return super().form_valid(form)


class PersonnelDetailView(LoginRequiredMixin, DetailView):
    """Détails d'un employé"""
    model = Personnel
    template_name = 'personnel/employe_detail.html'
    context_object_name = 'employe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['affectations'] = self.object.affectations.select_related('projet').order_by('-date_debut')
        context['affectations_actives'] = self.object.affectations.filter(date_fin__isnull=True)
        
        # Calculs financiers globaux
        context['salaire_du_total'] = self.object.get_salaire_du()
        context['total_paye'] = self.object.get_total_paiements()
        context['reste_a_payer'] = self.object.get_reste_a_payer()
        
        # Paiements détaillés par projet
        context['paiements_par_projet'] = self.object.get_paiements_par_projet()
        
        # Tous les paiements récents
        context['paiements_recents'] = self.object.paiements.select_related('projet').order_by('-date_paiement')[:10]
        
        return context


class PersonnelDeleteView(LoginRequiredMixin, DeleteView):
    """Suppression d'un employé"""
    model = Personnel
    template_name = 'personnel/employe_confirm_delete.html'
    success_url = reverse_lazy('personnel:employe_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personnel = self.object
        
        # Compter les éléments liés qui seront supprimés
        context['nb_affectations'] = personnel.affectations.count()
        context['nb_paiements'] = personnel.paiements.count()
        context['nb_taches_responsable'] = personnel.taches_responsable.count()
        
        # Calculs financiers
        context['total_paiements'] = personnel.get_total_paiements()
        context['salaire_du'] = personnel.get_salaire_du()
        
        # Total des éléments
        context['total_elements'] = (
            context['nb_affectations'] + 
            context['nb_paiements'] + 
            context['nb_taches_responsable']
        )
        
        return context
    
    def delete(self, request, *args, **kwargs):
        personnel_nom = self.get_object().get_full_name()
        messages.warning(request, f'Employé "{personnel_nom}" et toutes ses données associées ont été supprimés.')
        return super().delete(request, *args, **kwargs)


# ===== AFFECTATIONS =====
class AffectationListView(LoginRequiredMixin, ListView):
    """Liste des affectations"""
    model = AffectationPersonnel
    template_name = 'personnel/affectation_list.html'
    context_object_name = 'affectations'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AffectationPersonnel.objects.select_related('personnel', 'projet').order_by('-date_debut')
        
        # Filtre actives/terminées
        statut = self.request.GET.get('statut')
        if statut == 'actives':
            queryset = queryset.filter(date_fin__isnull=True)
        elif statut == 'terminees':
            queryset = queryset.filter(date_fin__isnull=False)
        
        return queryset


class AffectationCreateView(LoginRequiredMixin, CreateView):
    """Création d'une affectation"""
    model = AffectationPersonnel
    form_class = AffectationPersonnelForm
    template_name = 'personnel/affectation_form.html'
    success_url = reverse_lazy('personnel:affectation_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Affectation créée avec succès.')
        return super().form_valid(form)


class AffectationUpdateView(LoginRequiredMixin, UpdateView):
    """Modification d'une affectation"""
    model = AffectationPersonnel
    form_class = AffectationPersonnelForm
    template_name = 'personnel/affectation_form.html'
    success_url = reverse_lazy('personnel:affectation_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Affectation modifiée avec succès.')
        return super().form_valid(form)


@login_required
def terminer_affectation(request, pk):
    """Terminer une affectation"""
    affectation = get_object_or_404(AffectationPersonnel, pk=pk)
    
    if request.method == 'POST':
        from django.utils import timezone
        affectation.date_fin = timezone.now().date()
        affectation.save()
        messages.success(request, 'Affectation terminée avec succès.')
        return redirect('personnel:affectation_list')
    
    context = {'affectation': affectation}
    return render(request, 'personnel/affectation_terminer.html', context)


# ===== PAIEMENTS =====
class PaiementPersonnelListView(LoginRequiredMixin, ListView):
    """Liste des paiements du personnel"""
    model = PaiementPersonnel
    template_name = 'personnel/paiement_list.html'
    context_object_name = 'paiements'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PaiementPersonnel.objects.select_related('personnel', 'projet', 'saisi_par').order_by('-date_paiement')
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtre par personnel
        personnel_id = self.request.GET.get('personnel')
        if personnel_id:
            queryset = queryset.filter(personnel_id=personnel_id)
        
        # Filtre par projet
        projet_id = self.request.GET.get('projet')
        if projet_id:
            queryset = queryset.filter(projet_id=projet_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        from apps.projects.models import Projet
        
        context = super().get_context_data(**kwargs)
        
        # Liste des employés pour le filtre
        context['employes'] = Personnel.objects.filter(actif=True).order_by('nom', 'prenom')
        
        # Liste des projets pour le filtre
        context['projets'] = Projet.objects.filter(statut__in=['En_cours', 'Planifié']).order_by('code_projet')
        
        # Calcul du total des montants affichés
        queryset = self.get_queryset()
        context['total_montant'] = queryset.aggregate(total=Sum('montant'))['total'] or 0
        
        return context


class PaiementPersonnelCreateView(LoginRequiredMixin, CreateView):
    """Création d'un paiement"""
    model = PaiementPersonnel
    form_class = PaiementPersonnelForm
    template_name = 'personnel/paiement_form.html'
    success_url = reverse_lazy('personnel:paiement_list')
    
    def form_valid(self, form):
        form.instance.saisi_par = self.request.user
        messages.success(self.request, 'Paiement créé avec succès.')
        return super().form_valid(form)


class PaiementPersonnelUpdateView(LoginRequiredMixin, UpdateView):
    """Modification d'un paiement"""
    model = PaiementPersonnel
    form_class = PaiementPersonnelForm
    template_name = 'personnel/paiement_form.html'
    success_url = reverse_lazy('personnel:paiement_list')
    
    def get_queryset(self):
        # Seuls les paiements en attente peuvent être modifiés
        return PaiementPersonnel.objects.filter(statut='En_attente')
    
    def form_valid(self, form):
        messages.success(self.request, 'Paiement modifié avec succès.')
        return super().form_valid(form)


class PaiementPersonnelDetailView(LoginRequiredMixin, DetailView):
    """Détails d'un paiement"""
    model = PaiementPersonnel
    template_name = 'personnel/paiement_detail.html'
    context_object_name = 'paiement'


@login_required
def valider_paiement(request, pk):
    """Valider un paiement"""
    paiement = get_object_or_404(PaiementPersonnel, pk=pk)
    
    if paiement.statut != 'En_attente':
        messages.error(request, 'Ce paiement ne peut pas être validé.')
        return redirect('personnel:paiement_detail', pk=pk)
    
    if request.method == 'POST':
        from django.utils import timezone
        paiement.statut = 'Validé'
        paiement.date_validation = timezone.now()
        paiement.valide_par = request.user
        paiement.save()
        messages.success(request, f'Paiement de {paiement.montant} GNF validé avec succès.')
        return redirect('personnel:paiement_detail', pk=pk)
    
    context = {'paiement': paiement}
    return render(request, 'personnel/paiement_valider.html', context)


@login_required
def rejeter_paiement(request, pk):
    """Rejeter un paiement"""
    paiement = get_object_or_404(PaiementPersonnel, pk=pk)
    
    if paiement.statut != 'En_attente':
        messages.error(request, 'Ce paiement ne peut pas être rejeté.')
        return redirect('personnel:paiement_detail', pk=pk)
    
    if request.method == 'POST':
        from django.utils import timezone
        paiement.statut = 'Rejeté'
        paiement.date_validation = timezone.now()
        paiement.valide_par = request.user
        paiement.save()
        messages.warning(request, f'Paiement de {paiement.montant} GNF rejeté.')
        return redirect('personnel:paiement_detail', pk=pk)
    
    context = {'paiement': paiement}
    return render(request, 'personnel/paiement_rejeter.html', context)
