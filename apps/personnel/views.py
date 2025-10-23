from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from .models import Personnel, AffectationPersonnel
from .forms import PersonnelForm, AffectationPersonnelForm


@login_required
def personnel_home(request):
    """Page d'accueil du module personnel"""
    stats = {
        'total_personnel': Personnel.objects.count(),
        'personnel_actif': Personnel.objects.filter(actif=True).count(),
        'personnel_inactif': Personnel.objects.filter(actif=False).count(),
        'total_affectations': AffectationPersonnel.objects.filter(date_fin__isnull=True).count(),
    }
    
    personnel_recents = Personnel.objects.order_by('-date_embauche')[:5]
    affectations_actives = AffectationPersonnel.objects.filter(
        date_fin__isnull=True
    ).select_related('personnel', 'projet')[:5]
    
    context = {
        'stats': stats,
        'personnel_recents': personnel_recents,
        'affectations_actives': affectations_actives,
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
        
        # Filtre par poste
        poste = self.request.GET.get('poste')
        if poste:
            queryset = queryset.filter(poste=poste)
        
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
        return context


class PersonnelDeleteView(LoginRequiredMixin, DeleteView):
    """Suppression d'un employé"""
    model = Personnel
    template_name = 'personnel/employe_confirm_delete.html'
    success_url = reverse_lazy('personnel:employe_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Employé supprimé avec succès.')
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
