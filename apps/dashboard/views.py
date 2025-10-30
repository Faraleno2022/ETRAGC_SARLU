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
    
    # Statistiques financières GLOBALES (tous projets confondus)
    # Budget prévu total de tous les projets
    budget_prevu_total = Projet.objects.aggregate(
        total=Sum('montant_prevu')
    )['total'] or 0
    
    # Total des dépôts (tous projets)
    total_depots = Transaction.objects.filter(
        type='Dépôt',
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Total des retraits (tous projets)
    total_retraits = Transaction.objects.filter(
        type='Retrait',
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Total des dépenses via transactions (Achats + Dépenses + Paiements)
    total_depenses_transactions = Transaction.objects.filter(
        type='Dépense',
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Détail par catégorie de dépenses
    total_achats_materiaux = Transaction.objects.filter(
        type='Dépense',
        categorie='Achat Matériaux',
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    total_paiements_personnel = Transaction.objects.filter(
        type='Dépense',
        categorie='Paiement Personnel',
        statut='Validée'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    total_autres_depenses = Transaction.objects.filter(
        type='Dépense',
        statut='Validée'
    ).exclude(
        categorie__in=['Achat Matériaux', 'Paiement Personnel']
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Dépenses en attente de validation
    depenses_en_attente = Depense.objects.filter(statut='En_attente').count()
    
    # Calcul du montant global disponible
    # Montant Global = Budget Prévu + Dépôts - Retraits - Dépenses
    montant_global = budget_prevu_total + total_depots
    solde_disponible = montant_global - total_retraits - total_depenses_transactions
    
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
        # Statistiques générales
        'total_projets': total_projets,
        'projets_actifs': projets_actifs,
        'projets_termines': projets_termines,
        'total_clients': total_clients,
        
        # Statistiques financières globales
        'budget_prevu_total': budget_prevu_total,
        'montant_global': montant_global,
        'total_depots': total_depots,
        'total_retraits': total_retraits,
        'total_depenses_transactions': total_depenses_transactions,
        'solde_disponible': solde_disponible,
        
        # Détail des dépenses par catégorie
        'total_achats_materiaux': total_achats_materiaux,
        'total_paiements_personnel': total_paiements_personnel,
        'total_autres_depenses': total_autres_depenses,
        'depenses_en_attente': depenses_en_attente,
        
        # Listes
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
