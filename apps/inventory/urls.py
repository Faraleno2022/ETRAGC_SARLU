from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Dashboard
    path('', views.inventory_dashboard, name='dashboard'),
    
    # Produits
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('produits/nouveau/', views.produit_create, name='produit_create'),
    path('produits/<int:pk>/modifier/', views.produit_update, name='produit_update'),
    
    # Stocks
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('stocks/nouveau/', views.stock_create, name='stock_create'),
    
    # Achats
    path('achats/', views.achat_list, name='achat_list'),
    path('achats/<int:pk>/', views.achat_detail, name='achat_detail'),
    path('achats/nouveau/', views.achat_create, name='achat_create'),
    path('achats/<int:pk>/modifier/', views.achat_update, name='achat_update'),
    path('achats/<int:pk>/valider/', views.achat_valider, name='achat_valider'),
    path('achats/<int:pk>/recevoir/', views.achat_recevoir, name='achat_recevoir'),
    
    # Mouvements
    path('mouvements/', views.mouvement_list, name='mouvement_list'),
    path('mouvements/nouveau/', views.mouvement_create, name='mouvement_create'),
    
    # Alertes
    path('alertes/', views.alertes_stock, name='alertes_stock'),
]
