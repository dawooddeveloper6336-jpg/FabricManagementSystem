from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('backup/', views.backup_database, name='backup'),
    path('download/<str:filename>/', views.download_backup, name='download_backup'),
    path('history/', views.backup_history, name='backup_history'),
    path('restore/', views.restore_database, name='restore'),
    path('delete/<str:filename>/', views.delete_backup, name='delete_backup'),
]