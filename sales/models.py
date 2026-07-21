from django.db import models
from django.utils import timezone
from masters.models import Fabric
from inventory.models import FinishedStock

class SalesInvoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    invoice_date = models.DateField(default=timezone.now)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales_invoice'
        ordering = ['-invoice_date', '-created_at']

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last = SalesInvoice.objects.order_by('id').last()
            if last and last.invoice_number.startswith('INV-'):
                try:
                    num = int(last.invoice_number[4:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.invoice_number = f"INV-{num:06d}"
        super().save(*args, **kwargs)


class SalesInvoiceItem(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='items')
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    grade = models.CharField(max_length=10, choices=(('A', 'Grade A'), ('B', 'Grade B'), ('C', 'CP')))
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    rate = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    class Meta:
        db_table = 'sales_invoice_item'

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.fabric.fabric_code}"

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.rate
        super().save(*args, **kwargs)