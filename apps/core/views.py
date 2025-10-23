from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.projects.models import Projet
from apps.clients.models import Client
from apps.personnel.models import Personnel


@login_required
def home(request):
    """Page d'accueil de l'entreprise"""
    
    # Statistiques
    stats = {
        'total_projects': Projet.objects.count(),
        'total_clients': Client.objects.count(),
        'total_personnel': Personnel.objects.count(),
        'years_experience': '1+',
    }
    
    context = {
        'company_name': 'ÉLITE DES TRAVAUX DE GÉNIE CIVIL SARLU',
        'company_short': 'ETRAGC SARLU',
        'stats': stats,
    }
    return render(request, 'core/home.html', context)
