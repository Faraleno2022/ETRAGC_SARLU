from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    
    # Dépenses
    path('depenses/', views.DepenseListView.as_view(), name='depense_list'),
    path('depenses/create/', views.DepenseCreateView.as_view(), name='depense_create'),
    path('depenses/<int:pk>/', views.DepenseDetailView.as_view(), name='depense_detail'),
    path('depenses/<int:pk>/update/', views.DepenseUpdateView.as_view(), name='depense_update'),
    path('depenses/<int:pk>/valider/', views.depense_valider, name='depense_valider'),
    path('depenses/<int:pk>/rejeter/', views.depense_rejeter, name='depense_rejeter'),
    
    # Fournisseurs
    path('fournisseurs/', views.FournisseurListView.as_view(), name='fournisseur_list'),
    path('fournisseurs/create/', views.FournisseurCreateView.as_view(), name='fournisseur_create'),
    path('fournisseurs/<int:pk>/', views.FournisseurDetailView.as_view(), name='fournisseur_detail'),
    path('fournisseurs/<int:pk>/update/', views.FournisseurUpdateView.as_view(), name='fournisseur_update'),
    
    # Catégories
    path('categories/', views.CategorieDepenseListView.as_view(), name='categorie_list'),
    path('categories/create/', views.CategorieDepenseCreateView.as_view(), name='categorie_create'),
]
