from django.urls import path
from . import views

app_name = 'planning'

urlpatterns = [
    path('', views.planning_home, name='home'),
    path('taches/', views.TacheListView.as_view(), name='tache_list'),
    path('taches/nouvelle/', views.TacheCreateView.as_view(), name='tache_create'),
    path('taches/<int:pk>/', views.TacheDetailView.as_view(), name='tache_detail'),
    path('taches/<int:pk>/modifier/', views.TacheUpdateView.as_view(), name='tache_update'),
    path('taches/<int:pk>/supprimer/', views.TacheDeleteView.as_view(), name='tache_delete'),
    
    # Actions rapides
    path('taches/<int:pk>/terminer/', views.terminer_tache, name='tache_terminer'),
    path('taches/<int:pk>/demarrer/', views.demarrer_tache, name='tache_demarrer'),
    path('taches/<int:pk>/pause/', views.mettre_en_pause_tache, name='tache_pause'),
]
