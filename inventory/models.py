from django.db import models
from django.utils import timezone
from masters.models import Fabric, Manufacturer

# ---------- Greige Stock (unchanged) ----------
class GreigeStock(models.Model):
    fabric = models.OneToOneField(Fabric, on_delete=models.CASCADE, related_name='greige_stock')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    current_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reserved_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'greige_stock'
        verbose_name = 'Greige Stock'
        verbose_name_plural = 'Greige Stock'

    def __str__(self):
        return f"{self.fabric.fabric_code} - {self.current_stock}"

    @property
    def available_stock(self):
        return self.current_stock - self.reserved_stock


# ---------- Dispatch (unchanged) ----------
class Dispatch(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('returned', 'Returned'),
    )
    dispatch_number = models.CharField(max_length=20, unique=True, editable=False)
    dispatch_date = models.DateField(default=timezone.now)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    dispatch_quantity = models.DecimalField(max_digits=15, decimal_places=2)
    color = models.CharField(max_length=100, blank=True, null=True)
    shade = models.CharField(max_length=100, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    finish = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dispatch'
        ordering = ['-dispatch_date', '-created_at']

    def __str__(self):
        return self.dispatch_number

    def save(self, *args, **kwargs):
        if not self.dispatch_number:
            last = Dispatch.objects.order_by('id').last()
            if last and last.dispatch_number.startswith('DSP-'):
                try:
                    num = int(last.dispatch_number[4:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.dispatch_number = f"DSP-{num:06d}"
        super().save(*args, **kwargs)


# ---------- Dispatch Specification (unchanged) ----------
class DispatchSpecification(models.Model):
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='specifications')
    spec_name = models.CharField(max_length=100)
    spec_value = models.CharField(max_length=100)

    class Meta:
        db_table = 'dispatch_specification'
        verbose_name = 'Dispatch Specification'
        verbose_name_plural = 'Dispatch Specifications'

    def __str__(self):
        return f"{self.spec_name}: {self.spec_value}"


# ---------- Transit Stock (unchanged) ----------
class TransitStock(models.Model):
    fabric = models.OneToOneField(Fabric, on_delete=models.CASCADE, related_name='transit_stock')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    class Meta:
        db_table = 'transit_stock'
        unique_together = ('fabric', 'manufacturer')

    def __str__(self):
        return f"{self.fabric.fabric_code} - {self.quantity}"


# ---------- Processing Receiving (unchanged) ----------
class ProcessingReceiving(models.Model):
    receiving_number = models.CharField(max_length=20, unique=True, editable=False)
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='receivings')
    receiving_date = models.DateField(default=timezone.now)
    total_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_gain = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'processing_receiving'
        ordering = ['-receiving_date', '-created_at']

    def __str__(self):
        return self.receiving_number

    def save(self, *args, **kwargs):
        if not self.receiving_number:
            last = ProcessingReceiving.objects.order_by('id').last()
            if last and last.receiving_number.startswith('PRC-'):
                try:
                    num = int(last.receiving_number[4:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.receiving_number = f"PRC-{num:06d}"
        super().save(*args, **kwargs)

    @property
    def total_grade_a(self):
        return sum(g.grade_a for g in self.grades.all()) or 0

    @property
    def total_grade_b(self):
        return sum(g.grade_b for g in self.grades.all()) or 0

    @property
    def total_cp(self):
        return sum(g.cp for g in self.grades.all()) or 0


# ---------- Processing Receiving Grade (unchanged) ----------
class ProcessingReceivingGrade(models.Model):
    receiving = models.ForeignKey(ProcessingReceiving, on_delete=models.CASCADE, related_name='grades')
    color = models.CharField(max_length=100)
    dispatch_quantity = models.DecimalField(max_digits=15, decimal_places=2)
    grade_a = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    grade_b = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cp = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    received_qty = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    loss = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    gain = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    loss_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False)
    gain_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False)

    class Meta:
        db_table = 'processing_receiving_grade'
        unique_together = ('receiving', 'color')

    def save(self, *args, **kwargs):
        self.received_qty = self.grade_a + self.grade_b + self.cp
        self.loss = self.dispatch_quantity - self.received_qty
        self.gain = self.received_qty - self.dispatch_quantity
        if self.dispatch_quantity > 0:
            self.loss_percent = (self.loss / self.dispatch_quantity) * 100
            self.gain_percent = (self.gain / self.dispatch_quantity) * 100
        else:
            self.loss_percent = 0
            self.gain_percent = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receiving.receiving_number} - {self.color}"


# ---------- Finished Stock (UPDATED) ----------
class FinishedStock(models.Model):
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, default='')           # NEW
    grade_a = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    grade_b = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cp = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reserved = models.DecimalField(max_digits=15, decimal_places=2, default=0)   # NEW (for future)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'finished_stock'
        unique_together = ('fabric', 'manufacturer', 'color')      # UPDATED
        verbose_name = 'Finished Stock'
        verbose_name_plural = 'Finished Stock'

    def __str__(self):
        return f"{self.fabric.fabric_code} - {self.color}"

    @property
    def available_stock(self):
        return self.grade_a + self.grade_b + self.cp - self.reserved