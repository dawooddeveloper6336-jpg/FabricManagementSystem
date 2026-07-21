from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Greige Stock
    path('greige-stock/', views.GreigeStockListView.as_view(), name='greige_stock'),

    # Dispatch for Dyeing
    path('dispatch/', views.DispatchListView.as_view(), name='dispatch_list'),
    path('dispatch/add/', views.DispatchCreateView.as_view(), name='dispatch_add'),
    path('dispatch/edit/<int:pk>/', views.DispatchUpdateView.as_view(), name='dispatch_edit'),
    path('dispatch/delete/<int:pk>/', views.DispatchDeleteView.as_view(), name='dispatch_delete'),
    path('dispatch/print/<int:pk>/', views.DispatchPrintView.as_view(), name='dispatch_print'),

    # Processing In Transit
    path('processing-transit/', views.ProcessingTransitListView.as_view(), name='processing_transit'),

    # Processing Receiving
    path('processing-receiving/', views.ProcessingReceivingListView.as_view(), name='processing_receiving_list'),
    path('processing-receiving/add/', views.ProcessingReceivingCreateView.as_view(), name='processing_receiving_add'),
    path('processing-receiving/edit/<int:pk>/', views.ProcessingReceivingUpdateView.as_view(), name='processing_receiving_edit'),
    path('processing-receiving/delete/<int:pk>/', views.ProcessingReceivingDeleteView.as_view(), name='processing_receiving_delete'),
    path('processing-receiving/print/<int:pk>/', views.ProcessingReceivingPrintView.as_view(), name='processing_receiving_print'),

    # AJAX
    path('ajax/dispatch-colors/', views.get_dispatch_colors, name='dispatch_colors'),

    # ========== NEW ==========
    path('finished-stock/', views.FinishedStockListView.as_view(), name='finished_stock'),
]