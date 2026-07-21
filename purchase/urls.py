from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    # Purchase Orders
    path('purchase-orders/', views.PurchaseOrderListView.as_view(), name='po_list'),
    path('purchase-orders/add/', views.PurchaseOrderCreateView.as_view(), name='po_add'),
    path('purchase-orders/edit/<int:pk>/', views.PurchaseOrderUpdateView.as_view(), name='po_edit'),
    path('purchase-orders/delete/<int:pk>/', views.PurchaseOrderDeleteView.as_view(), name='po_delete'),
    path('purchase-orders/print/<int:pk>/', views.PurchaseOrderPrintView.as_view(), name='po_print'),

    # Purchase Receivings
    path('receivings/', views.PurchaseReceivingListView.as_view(), name='receiving_list'),
    path('receivings/add/', views.PurchaseReceivingCreateView.as_view(), name='receiving_add'),
    path('receivings/edit/<int:pk>/', views.PurchaseReceivingUpdateView.as_view(), name='receiving_edit'),
    path('receivings/delete/<int:pk>/', views.PurchaseReceivingDeleteView.as_view(), name='receiving_delete'),
    path('receivings/print/<int:pk>/', views.PurchaseReceivingPrintView.as_view(), name='receiving_print'),

    # AJAX
    path('ajax/fabric-details/', views.get_fabric_details, name='fabric_details'),
    path('ajax/po-details/', views.get_po_details, name='po_details'),
]