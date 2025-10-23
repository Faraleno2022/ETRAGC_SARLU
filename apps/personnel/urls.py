from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    path('', views.personnel_home, name='home'),
    
    # Personnel
    path('employes/', views.PersonnelListView.as_view(), name='employe_list'),
    path('employes/nouveau/', views.PersonnelCreateView.as_view(), name='employe_create'),
    path('employes/<int:pk>/', views.PersonnelDetailView.as_view(), name='employe_detail'),
    path('employes/<int:pk>/modifier/', views.PersonnelUpdateView.as_view(), name='employe_update'),
    path('employes/<int:pk>/supprimer/', views.PersonnelDeleteView.as_view(), name='employe_delete'),
    
    # Affectations
    path('affectations/', views.AffectationListView.as_view(), name='affectation_list'),
    path('affectations/nouvelle/', views.AffectationCreateView.as_view(), name='affectation_create'),
    path('affectations/<int:pk>/modifier/', views.AffectationUpdateView.as_view(), name='affectation_update'),
    path('affectations/<int:pk>/terminer/', views.terminer_affectation, name='affectation_terminer'),
]
