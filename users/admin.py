from django.contrib import admin
from .models import CustomUser, Vendor, PhoneNumber


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'credit']


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'total_amount_added']
