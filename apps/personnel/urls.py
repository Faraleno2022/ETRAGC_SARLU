from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    path('', views.personnel_home, name='home'),
    
    # Personnel
    path('employes/', views.PersonnelListView.as_view(), name='employe_list'),
    path('employes/nouveau/', views.PersonnelCreateView.as_view(), name='create'),
    path('employes/<int:pk>/', views.PersonnelDetailView.as_view(), name='detail'),
    path('employes/<int:pk>/modifier/', views.PersonnelUpdateView.as_view(), name='update'),
    path('employes/<int:pk>/supprimer/', views.PersonnelDeleteView.as_view(), name='delete'),
    
    # Affectations
    path('affectations/', views.AffectationListView.as_view(), name='affectation_list'),
    path('affectations/nouvelle/', views.AffectationCreateView.as_view(), name='affectation_create'),
    path('affectations/<int:pk>/modifier/', views.AffectationUpdateView.as_view(), name='affectation_update'),
    path('affectations/<int:pk>/terminer/', views.terminer_affectation, name='affectation_terminer'),
    
    # Paiements
    path('paiements/', views.PaiementPersonnelListView.as_view(), name='paiement_list'),
    path('paiements/nouveau/', views.PaiementPersonnelCreateView.as_view(), name='paiement_create'),
    path('paiements/<int:pk>/', views.PaiementPersonnelDetailView.as_view(), name='paiement_detail'),
    path('paiements/<int:pk>/modifier/', views.PaiementPersonnelUpdateView.as_view(), name='paiement_update'),
    path('paiements/<int:pk>/valider/', views.valider_paiement, name='paiement_valider'),
    path('paiements/<int:pk>/rejeter/', views.rejeter_paiement, name='paiement_rejeter'),
]
