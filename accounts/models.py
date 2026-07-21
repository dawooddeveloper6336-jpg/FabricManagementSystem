from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('purchase', 'Purchase'),
        ('store', 'Store'),
        ('sales', 'Sales'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='store')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    class Meta:
        permissions = [
            ("can_view_masters", "Can view Masters module"),
            ("can_view_purchase", "Can view Purchase module"),
            ("can_view_inventory", "Can view Inventory module"),
            ("can_view_sales", "Can view Sales module"),
            ("can_view_reports", "Can view Reports module"),
            ("can_manage_users", "Can manage users"),
        ]