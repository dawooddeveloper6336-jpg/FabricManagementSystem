from django.db import models
from django.utils import timezone

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=200, default='Fabric Management System')
    logo = models.ImageField(upload_to='settings/logo/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    ntn = models.CharField(max_length=50, blank=True, null=True, verbose_name='NTN / Tax Number')
    currency = models.CharField(max_length=10, default='PKR')
    default_unit = models.CharField(max_length=10, default='MTR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings_company_info'
        verbose_name = 'Company Information'
        verbose_name_plural = 'Company Information'

    def __str__(self):
        return self.company_name


class InvoiceSettings(models.Model):
    invoice_prefix = models.CharField(max_length=20, default='INV-')
    po_prefix = models.CharField(max_length=20, default='PO-')
    dispatch_prefix = models.CharField(max_length=20, default='DSP-')
    sales_prefix = models.CharField(max_length=20, default='SAL-')
    invoice_footer = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings_invoice'
        verbose_name = 'Invoice Setting'
        verbose_name_plural = 'Invoice Settings'

    def __str__(self):
        return "Invoice Settings"


class AppearanceSettings(models.Model):
    THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    )
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='system')
    primary_color = models.CharField(max_length=7, default='#2c3e50')
    sidebar_style = models.CharField(max_length=20, default='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings_appearance'
        verbose_name = 'Appearance Setting'
        verbose_name_plural = 'Appearance Settings'

    def __str__(self):
        return "Appearance Settings"