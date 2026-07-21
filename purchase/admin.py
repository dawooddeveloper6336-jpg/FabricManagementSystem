from django.contrib import admin
from .models import PurchaseOrder, PurchaseReceiving

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'po_date', 'manufacturer', 'buying_house', 'fabric', 'order_quantity', 'status', 'revision_number', 'created_at')
    list_filter = ('status', 'po_date', 'manufacturer')
    search_fields = ('po_number', 'manufacturer__manufacturer_name')
    readonly_fields = ('po_number', 'revision_number')

@admin.register(PurchaseReceiving)
class PurchaseReceivingAdmin(admin.ModelAdmin):
    list_display = ('receiving_number', 'purchase_order', 'receive_date', 'received_quantity', 'challan_number', 'created_at')
    list_filter = ('receive_date',)
    search_fields = ('receiving_number', 'purchase_order__po_number', 'challan_number')
    readonly_fields = ('receiving_number',)