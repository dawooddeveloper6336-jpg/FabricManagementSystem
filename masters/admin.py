from django.contrib import admin
from .models import Manufacturer, BuyingHouse

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('manufacturer_name', 'contact_person', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('manufacturer_name', 'contact_person', 'phone', 'email')

@admin.register(BuyingHouse)
class BuyingHouseAdmin(admin.ModelAdmin):
    list_display = ('buying_house_name', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('buying_house_name', 'phone', 'email')

from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_name', 'commission_percentage', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('agent_name', 'phone', 'email')

from .models import Fabric

@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('fabric_code', 'fabric_blend', 'fabric_quality', 'weave', 'unit', 'status', 'created_at')
    list_filter = ('status', 'unit', 'weave')
    search_fields = ('fabric_code', 'fabric_blend', 'fabric_quality')
    readonly_fields = ('fabric_code',)