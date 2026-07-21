from django.db import models
from django.utils import timezone

# ---------- Manufacturer ----------
class Manufacturer(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    manufacturer_name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manufacturer'
        ordering = ['-created_at']
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return self.manufacturer_name


# ---------- Buying House ----------
class BuyingHouse(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    buying_house_name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'buying_house'
        ordering = ['-created_at']
        verbose_name = 'Buying House'
        verbose_name_plural = 'Buying Houses'

    def __str__(self):
        return self.buying_house_name
# ---------- Agent ----------
class Agent(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    agent_name = models.CharField(max_length=200, unique=True)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Between 0 and 100")
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agent'
        ordering = ['-created_at']
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def __str__(self):
        return self.agent_name

# ---------- Fabric ----------
class Fabric(models.Model):
    UNIT_CHOICES = (
        ('MTR', 'Meter (MTR)'),
        ('YARD', 'Yard'),
        ('KG', 'Kilogram'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    fabric_code = models.CharField(max_length=20, unique=True, editable=False)
    fabric_blend = models.CharField(max_length=100)
    fabric_quality = models.CharField(max_length=100)
    warp = models.CharField(max_length=50)
    warp_blend = models.CharField(max_length=50, blank=True, null=True)
    weft = models.CharField(max_length=50)
    weft_blend = models.CharField(max_length=50, blank=True, null=True)
    ends = models.PositiveIntegerField()
    picks = models.PositiveIntegerField()
    weave = models.CharField(max_length=50)
    greige_width_on_loom = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    greige_width_off_loom = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    selvedge_type = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='MTR')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fabric'
        ordering = ['-created_at']
        verbose_name = 'Fabric'
        verbose_name_plural = 'Fabrics'

    def __str__(self):
        return f"{self.fabric_code} - {self.fabric_blend}"

    def save(self, *args, **kwargs):
        if not self.fabric_code:
            # Generate next code like FAB0001
            last = Fabric.objects.order_by('id').last()
            if last and last.fabric_code.startswith('FAB'):
                try:
                    num = int(last.fabric_code[3:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.fabric_code = f"FAB{num:04d}"
        super().save(*args, **kwargs)