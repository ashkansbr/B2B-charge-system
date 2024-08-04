from django.db import models, transaction
from credit_management.models import Vendor
from users.models import PhoneNumber
from django.core.exceptions import ValidationError
from credit_management.models import TransactionLog


class TopUp(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            vendor = Vendor.objects.select_for_update().get(pk=self.vendor.pk)
            if vendor.credit < self.amount:
                raise ValidationError({"detail": "Insufficient credit"})
            vendor.adjust_credit(-self.amount)
            phone_number = PhoneNumber.objects.select_for_update().get(pk=self.phone_number.pk)
            phone_number.total_amount_added += self.amount
            phone_number.save()
            super().save(*args, **kwargs)
            TransactionLog.objects.create(
                vendor=self.vendor,
                amount=self.amount,
                transaction_type=TransactionLog.TOPUP
            )

    def __str__(self):
        return f"TopUp: {self.phone_number.number} - Amount: {self.amount}"
