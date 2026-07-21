from django.contrib import admin
from .models import SalesInvoice, SalesInvoiceItem

@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_date', 'customer_name', 'total_amount', 'created_at')
    list_filter = ('invoice_date',)
    search_fields = ('invoice_number', 'customer_name')
    readonly_fields = ('invoice_number',)

@admin.register(SalesInvoiceItem)
class SalesInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'fabric', 'color', 'grade', 'quantity', 'rate', 'amount')
    search_fields = ('fabric__fabric_code',)