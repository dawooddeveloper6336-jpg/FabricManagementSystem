from django.db import models
from django.utils import timezone
from masters.models import Manufacturer, BuyingHouse, Agent, Fabric


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    po_number = models.CharField(max_length=20, unique=True, editable=False)
    po_date = models.DateField(default=timezone.now)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    buying_house = models.ForeignKey(BuyingHouse, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    agent_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    order_quantity = models.DecimalField(max_digits=15, decimal_places=2)
    tolerance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    delivery_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='purchase_orders')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Revision fields
    revision_number = models.PositiveIntegerField(default=0, editable=False)
    revision_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'purchase_order'
        ordering = ['-po_date', '-created_at']
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if not self.po_number:
            last = PurchaseOrder.objects.order_by('id').last()
            if last and last.po_number.startswith('PO-'):
                try:
                    num = int(last.po_number[3:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.po_number = f"PO-{num:06d}"
        super().save(*args, **kwargs)


class PurchaseReceiving(models.Model):
    receiving_number = models.CharField(max_length=20, unique=True, editable=False)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='receivings')
    receive_date = models.DateField(default=timezone.now)
    challan_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    received_quantity = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='receivings')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchase_receiving'
        ordering = ['-receive_date', '-created_at']
        verbose_name = 'Purchase Receiving'
        verbose_name_plural = 'Purchase Receivings'

    def __str__(self):
        return self.receiving_number

    def save(self, *args, **kwargs):
        if not self.receiving_number:
            last = PurchaseReceiving.objects.order_by('id').last()
            if last and last.receiving_number.startswith('PR-'):
                try:
                    num = int(last.receiving_number[3:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.receiving_number = f"PR-{num:06d}"
        super().save(*args, **kwargs)

    @classmethod
    def get_total_received(cls, purchase_order):
        total = cls.objects.filter(purchase_order=purchase_order).aggregate(
            total=models.Sum('received_quantity')
        )['total'] or 0
        return total

    @classmethod
    def get_remaining_quantity(cls, purchase_order):
        ordered = purchase_order.order_quantity
        received = cls.get_total_received(purchase_order)
        return ordered - received