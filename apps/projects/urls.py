from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjetListView.as_view(), name='list'),
    path('<int:pk>/', views.ProjetDetailView.as_view(), name='detail'),
    path('create/', views.ProjetCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProjetUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProjetDeleteView.as_view(), name='delete'),
]
