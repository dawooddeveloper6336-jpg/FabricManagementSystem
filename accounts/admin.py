from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'status', 'is_active', 'created_at')
    list_filter = ('role', 'status', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone', 'address', 'profile_image', 'role', 'status', 'created_at', 'updated_at')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('phone', 'address', 'profile_image', 'role', 'status')}),
    )
    readonly_fields = ('created_at', 'updated_at')