from django.contrib import admin
from .models import GreigeStock, Dispatch, DispatchSpecification, TransitStock

# Existing registration (keep)
@admin.register(GreigeStock)
class GreigeStockAdmin(admin.ModelAdmin):
    list_display = ('fabric', 'manufacturer', 'current_stock', 'reserved_stock', 'available_stock', 'last_updated')
    list_filter = ('manufacturer',)
    search_fields = ('fabric__fabric_code', 'fabric__fabric_blend', 'manufacturer__manufacturer_name')
    readonly_fields = ('available_stock',)

# New registrations for Dispatch
@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ('dispatch_number', 'dispatch_date', 'fabric', 'manufacturer', 'dispatch_quantity', 'status', 'created_at')
    list_filter = ('status', 'dispatch_date')
    search_fields = ('dispatch_number', 'fabric__fabric_code', 'manufacturer__manufacturer_name')
    readonly_fields = ('dispatch_number',)

@admin.register(DispatchSpecification)
class DispatchSpecificationAdmin(admin.ModelAdmin):
    list_display = ('dispatch', 'spec_name', 'spec_value')
    search_fields = ('spec_name', 'spec_value')

@admin.register(TransitStock)
class TransitStockAdmin(admin.ModelAdmin):
    list_display = ('fabric', 'manufacturer', 'quantity')
    search_fields = ('fabric__fabric_code', 'manufacturer__manufacturer_name')

from .models import ProcessingReceiving, ProcessingReceivingGrade, FinishedStock

@admin.register(ProcessingReceiving)
class ProcessingReceivingAdmin(admin.ModelAdmin):
    list_display = ('receiving_number', 'dispatch', 'receiving_date', 'total_received', 'created_at')
    list_filter = ('receiving_date',)
    search_fields = ('receiving_number', 'dispatch__dispatch_number')
    readonly_fields = ('receiving_number',)

@admin.register(ProcessingReceivingGrade)
class ProcessingReceivingGradeAdmin(admin.ModelAdmin):
    list_display = ('receiving', 'color', 'grade_a', 'grade_b', 'cp', 'received_qty', 'loss', 'gain')
    search_fields = ('color',)

@admin.register(FinishedStock)
class FinishedStockAdmin(admin.ModelAdmin):
    list_display = ('fabric', 'manufacturer', 'grade_a', 'grade_b', 'cp', 'last_updated')
    search_fields = ('fabric__fabric_code', 'manufacturer__manufacturer_name')