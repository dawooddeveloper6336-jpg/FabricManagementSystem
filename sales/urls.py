from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('invoices/', views.SalesInvoiceListView.as_view(), name='invoice_list'),
    path('invoices/add/', views.SalesInvoiceCreateView.as_view(), name='invoice_add'),
    path('invoices/edit/<int:pk>/', views.SalesInvoiceUpdateView.as_view(), name='invoice_edit'),
    path('invoices/delete/<int:pk>/', views.SalesInvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoices/print/<int:pk>/', views.SalesInvoicePrintView.as_view(), name='invoice_print'),
]