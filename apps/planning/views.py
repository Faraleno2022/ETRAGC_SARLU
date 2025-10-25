from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from .models import Tache
from .forms import TacheForm


@login_required
def planning_home(request):
    """Page d'accueil du module planning"""
    stats = {
        'total_taches': Tache.objects.count(),
        'taches_a_faire': Tache.objects.filter(statut='A_faire').count(),
        'taches_en_cours': Tache.objects.filter(statut='En_cours').count(),
        'taches_terminees': Tache.objects.filter(statut='Terminée').count(),
        'taches_en_retard': Tache.objects.filter(
            statut__in=['A_faire', 'En_cours', 'En_pause']
        ).filter(date_fin_prevue__lt=timezone.now().date()).count(),
    }
    
    taches_recentes = Tache.objects.select_related('projet', 'responsable').order_by('-date_creation')[:5]
    taches_urgentes = Tache.objects.filter(
        priorite='Critique',
        statut__in=['A_faire', 'En_cours']
    ).select_related('projet', 'responsable').order_by('date_fin_prevue')[:5]
    
    context = {
        'stats': stats,
        'taches_recentes': taches_recentes,
        'taches_urgentes': taches_urgentes,
    }
    return render(request, 'planning/home.html', context)


class TacheListView(LoginRequiredMixin, ListView):
    """Liste des tâches"""
    model = Tache
    template_name = 'planning/tache_list.html'
    context_object_name = 'taches'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Tache.objects.select_related('projet', 'responsable', 'tache_parent').order_by('-date_creation')
        
        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom_tache__icontains=search) |
                Q(description__icontains=search) |
                Q(projet__nom_projet__icontains=search)
            )
        
        # Filtre par statut
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Filtre par priorité
        priorite = self.request.GET.get('priorite')
        if priorite:
            queryset = queryset.filter(priorite=priorite)
        
        # Filtre par projet
        projet = self.request.GET.get('projet')
        if projet:
            queryset = queryset.filter(projet_id=projet)
        
        # Filtre tâches en retard
        retard = self.request.GET.get('retard')
        if retard:
            queryset = queryset.filter(
                statut__in=['A_faire', 'En_cours', 'En_pause'],
                date_fin_prevue__lt=timezone.now().date()
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.projects.models import Projet
        context['projets'] = Projet.objects.filter(statut='En_cours')
        context['statuts'] = Tache.STATUT_CHOICES
        context['priorites'] = Tache.PRIORITE_CHOICES
        return context


class TacheCreateView(LoginRequiredMixin, CreateView):
    """Créer une nouvelle tâche"""
    model = Tache
    form_class = TacheForm
    template_name = 'planning/tache_form.html'
    success_url = reverse_lazy('planning:tache_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tâche créée avec succès!')
        return super().form_valid(form)


class TacheUpdateView(LoginRequiredMixin, UpdateView):
    """Modifier une tâche"""
    model = Tache
    form_class = TacheForm
    template_name = 'planning/tache_form.html'
    success_url = reverse_lazy('planning:tache_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tâche modifiée avec succès!')
        return super().form_valid(form)


class TacheDetailView(LoginRequiredMixin, DetailView):
    """Détails d'une tâche"""
    model = Tache
    template_name = 'planning/tache_detail.html'
    context_object_name = 'tache'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sous_taches'] = self.object.sous_taches.all()
        return context


class TacheDeleteView(LoginRequiredMixin, DeleteView):
    """Supprimer une tâche"""
    model = Tache
    template_name = 'planning/tache_confirm_delete.html'
    success_url = reverse_lazy('planning:tache_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tâche supprimée avec succès!')
        return super().delete(request, *args, **kwargs)


from django.utils import timezone


@login_required
def changer_statut_tache(request, pk, nouveau_statut):
    """Changer rapidement le statut d'une tâche"""
    tache = get_object_or_404(Tache, pk=pk)
    
    statuts_valides = dict(Tache.STATUT_CHOICES).keys()
    if nouveau_statut in statuts_valides:
        tache.statut = nouveau_statut
        
        # Si terminée, enregistrer la date de fin réelle
        if nouveau_statut == 'Terminée' and not tache.date_fin_reelle:
            tache.date_fin_reelle = timezone.now().date()
            tache.pourcentage_progression = 100
        
        tache.save()
        messages.success(request, f'Statut de la tâche changé en "{tache.get_statut_display()}"')
    else:
        messages.error(request, 'Statut invalide')
    
    return redirect('planning:tache_detail', pk=pk)


@login_required
def terminer_tache(request, pk):
    """Marquer une tâche comme terminée"""
    return changer_statut_tache(request, pk, 'Terminée')


@login_required
def demarrer_tache(request, pk):
    """Démarrer une tâche"""
    return changer_statut_tache(request, pk, 'En_cours')


@login_required
def mettre_en_pause_tache(request, pk):
    """Mettre une tâche en pause"""
    return changer_statut_tache(request, pk, 'En_pause')
