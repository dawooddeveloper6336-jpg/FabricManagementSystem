from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('purchase/', views.purchase_report, name='purchase'),
    path('receiving/', views.receiving_report, name='receiving'),
    path('dispatch/', views.dispatch_report, name='dispatch'),
    path('processing/', views.processing_report, name='processing'),
    path('stock/', views.stock_report, name='stock'),
    path('sales/', views.sales_report, name='sales'),
]