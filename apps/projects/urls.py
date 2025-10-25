from django.urls import path
from . import views
from . import exports

app_name = 'projects'

urlpatterns = [
    path('', views.ProjetListView.as_view(), name='list'),
    path('<int:pk>/', views.ProjetDetailView.as_view(), name='detail'),
    path('create/', views.ProjetCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProjetUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProjetDeleteView.as_view(), name='delete'),
    
    # Exports
    path('export/excel/', exports.export_projets_excel, name='export_excel'),
    path('export/pdf/', exports.export_projets_pdf, name='export_pdf'),
    path('<int:pk>/export/pdf/', exports.export_projet_detail_pdf, name='export_detail_pdf'),
]
