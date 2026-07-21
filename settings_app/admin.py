from django.contrib import admin
from .models import CompanyInfo, InvoiceSettings, AppearanceSettings

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'updated_at')

@admin.register(InvoiceSettings)
class InvoiceSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_prefix', 'po_prefix')

@admin.register(AppearanceSettings)
class AppearanceSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'primary_color')