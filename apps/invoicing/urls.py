from django.urls import path
from . import views
from . import exports

app_name = 'invoicing'

urlpatterns = [
    path('', views.invoicing_home, name='home'),
    
    # Devis
    path('devis/', views.DevisListView.as_view(), name='devis_list'),
    path('devis/nouveau/', views.DevisCreateView.as_view(), name='devis_create'),
    path('devis/<int:pk>/', views.DevisDetailView.as_view(), name='devis_detail'),
    path('devis/<int:pk>/modifier/', views.DevisUpdateView.as_view(), name='devis_update'),
    path('devis/<int:pk>/supprimer/', views.DevisDeleteView.as_view(), name='devis_delete'),
    
    # Exports Devis
    path('devis/export/excel/', exports.export_devis_excel, name='devis_export_excel'),
    path('devis/export/pdf/', exports.export_devis_pdf, name='devis_export_pdf'),
    path('devis/<int:pk>/export/pdf/', exports.export_devis_detail_pdf, name='devis_export_detail_pdf'),
    
    # Factures
    path('factures/', views.FactureListView.as_view(), name='facture_list'),
    path('factures/nouvelle/', views.FactureCreateView.as_view(), name='facture_create'),
    path('factures/<int:pk>/', views.FactureDetailView.as_view(), name='facture_detail'),
    path('factures/<int:pk>/modifier/', views.FactureUpdateView.as_view(), name='facture_update'),
    path('factures/<int:pk>/supprimer/', views.FactureDeleteView.as_view(), name='facture_delete'),
    path('factures/<int:pk>/paiement/', views.ajouter_paiement, name='ajouter_paiement'),
    
    # Exports Factures
    path('factures/export/excel/', exports.export_factures_excel, name='factures_export_excel'),
    path('factures/export/pdf/', exports.export_factures_pdf, name='factures_export_pdf'),
    path('factures/<int:pk>/export/pdf/', exports.export_facture_detail_pdf, name='facture_export_detail_pdf'),
]
