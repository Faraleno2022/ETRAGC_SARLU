from django.urls import path
from . import views

app_name = 'invoicing'

urlpatterns = [
    path('', views.invoicing_home, name='home'),
    
    # Devis
    path('devis/', views.DevisListView.as_view(), name='devis_list'),
    path('devis/nouveau/', views.DevisCreateView.as_view(), name='devis_create'),
    path('devis/<int:pk>/', views.DevisDetailView.as_view(), name='devis_detail'),
    path('devis/<int:pk>/modifier/', views.DevisUpdateView.as_view(), name='devis_update'),
    
    # Factures
    path('factures/', views.FactureListView.as_view(), name='facture_list'),
    path('factures/nouvelle/', views.FactureCreateView.as_view(), name='facture_create'),
    path('factures/<int:pk>/', views.FactureDetailView.as_view(), name='facture_detail'),
    path('factures/<int:pk>/modifier/', views.FactureUpdateView.as_view(), name='facture_update'),
    path('factures/<int:pk>/paiement/', views.ajouter_paiement, name='ajouter_paiement'),
]
