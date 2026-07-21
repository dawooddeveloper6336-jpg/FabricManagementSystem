from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('masters/', include('masters.urls')),
    path('purchase/', include('purchase.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),          # already added
    path('reports/', include('reports.urls')),      # <-- ADD THIS
    path('settings/', include('settings_app.urls')),
    path('', RedirectView.as_view(url='accounts/login/', permanent=False), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)