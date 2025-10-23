"""
URL configuration for ETRAGC SARLU project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', include('apps.core.urls')),
    
    # App URLs
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('clients/', include('apps.clients.urls')),
    path('projects/', include('apps.projects.urls')),
    path('finances/', include('apps.finances.urls')),
    path('invoicing/', include('apps.invoicing.urls')),
    path('personnel/', include('apps.personnel.urls')),
    path('planning/', include('apps.planning.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
