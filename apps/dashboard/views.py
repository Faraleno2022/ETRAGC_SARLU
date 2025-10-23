from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.projects.models import Projet
from apps.finances.models import Transaction, Depense, CategorieDepense
from apps.clients.models import Client


@login_required
def dashboard_home(request):
    """Vue principale du tableau de bord"""
    
    # Statistiques générales
    total_projets = Projet.objects.count()
    projets_actifs = Projet.objects.filter(statut='En_cours').count()
    projets_termines = Projet.objects.filter(statut='Terminé').count()
    total_clients = Client.objects.filter(actif=True).count()
    
    # Statistiques financières
    total_depots = Transaction.objects.filter(type='Dépôt').aggregate(
        total=Sum('montant')
    )['total'] or 0
    
    total_retraits = Transaction.objects.filter(type='Retrait').aggregate(
        total=Sum('montant')
    )['total'] or 0
    
    total_depenses_validees = Depense.objects.filter(statut='Validée').aggregate(
        total=Sum('montant')
    )['total'] or 0
    
    depenses_en_attente = Depense.objects.filter(statut='En_attente').count()
    
    solde_global = total_depots - total_retraits
    
    # Projets récents
    projets_recents = Projet.objects.all()[:5]
    
    # Projets en retard
    from datetime import date
    projets_en_retard = Projet.objects.filter(
        date_fin_prevue__lt=date.today(),
        statut__in=['Planifié', 'En_cours']
    )[:5]
    
    # Projets avec budget dépassé
    projets_budget_depasse = []
    for projet in Projet.objects.filter(statut__in=['Planifié', 'En_cours']):
        if projet.is_budget_depasse():
            projets_budget_depasse.append(projet)
            if len(projets_budget_depasse) >= 5:
                break
    
    # Dépenses par catégorie (pour graphique)
    depenses_par_categorie = CategorieDepense.objects.annotate(
        total=Sum('depenses__montant', filter=Q(depenses__statut='Validée'))
    ).order_by('-total')[:10]
    
    # Transactions récentes
    transactions_recentes = Transaction.objects.all()[:10]
    
    # Dépenses récentes en attente de validation
    depenses_attente = Depense.objects.filter(statut='En_attente')[:10]
    
    context = {
        'total_projets': total_projets,
        'projets_actifs': projets_actifs,
        'projets_termines': projets_termines,
        'total_clients': total_clients,
        'total_depots': total_depots,
        'total_retraits': total_retraits,
        'total_depenses_validees': total_depenses_validees,
        'depenses_en_attente': depenses_en_attente,
        'solde_global': solde_global,
        'projets_recents': projets_recents,
        'projets_en_retard': projets_en_retard,
        'projets_budget_depasse': projets_budget_depasse,
        'depenses_par_categorie': depenses_par_categorie,
        'transactions_recentes': transactions_recentes,
        'depenses_attente': depenses_attente,
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def statistiques_view(request):
    """Vue des statistiques détaillées"""
    
    # Statistiques par période
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)
    
    # Transactions du mois
    transactions_mois = Transaction.objects.filter(
        date_transaction__gte=start_of_month
    )
    depots_mois = transactions_mois.filter(type='Dépôt').aggregate(
        total=Sum('montant')
    )['total'] or 0
    retraits_mois = transactions_mois.filter(type='Retrait').aggregate(
        total=Sum('montant')
    )['total'] or 0
    
    # Dépenses du mois
    depenses_mois = Depense.objects.filter(
        date_depense__gte=start_of_month,
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Transactions de l'année
    transactions_annee = Transaction.objects.filter(
        date_transaction__gte=start_of_year
    )
    depots_annee = transactions_annee.filter(type='Dépôt').aggregate(
        total=Sum('montant')
    )['total'] or 0
    retraits_annee = transactions_annee.filter(type='Retrait').aggregate(
        total=Sum('montant')
    )['total'] or 0
    
    # Dépenses de l'année
    depenses_annee = Depense.objects.filter(
        date_depense__gte=start_of_year,
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Statistiques par statut de projet
    projets_par_statut = Projet.objects.values('statut').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Top 5 projets par budget
    top_projets_budget = Projet.objects.order_by('-montant_prevu')[:5]
    
    # Top 5 projets par dépenses
    top_projets_depenses = []
    for projet in Projet.objects.all():
        projet.total_depenses = projet.get_total_depenses()
        top_projets_depenses.append(projet)
    top_projets_depenses.sort(key=lambda x: x.total_depenses, reverse=True)
    top_projets_depenses = top_projets_depenses[:5]
    
    context = {
        'depots_mois': depots_mois,
        'retraits_mois': retraits_mois,
        'depenses_mois': depenses_mois,
        'depots_annee': depots_annee,
        'retraits_annee': retraits_annee,
        'depenses_annee': depenses_annee,
        'projets_par_statut': projets_par_statut,
        'top_projets_budget': top_projets_budget,
        'top_projets_depenses': top_projets_depenses,
    }
    
    return render(request, 'dashboard/statistiques.html', context)
