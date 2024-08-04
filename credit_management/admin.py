from django.contrib import admin
from .models import CreditRequest, TransactionLog


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'amount', 'is_approved', 'created_at', 'approved_at']

    def save_model(self, request, obj, form, change):
        if 'is_approved' in form.changed_data and obj.is_approved:
            obj.approve()
        super().save_model(request, obj, form, change)


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'amount', 'transaction_type', 'created_at']
