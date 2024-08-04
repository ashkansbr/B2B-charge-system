from django.db import models, transaction
from django.utils import timezone
from users.models import Vendor
from common.basemodel import BaseModel
from rest_framework.exceptions import ValidationError


class CreditRequest(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    def approve(self):
        with transaction.atomic():
            credit_request = CreditRequest.objects.select_for_update().get(pk=self.pk)
            if credit_request.is_approved:
                raise ValidationError("This request has already been approved")
            credit_request.is_approved = True
            credit_request.approved_at = timezone.now()
            vendor = Vendor.objects.select_for_update().get(pk=self.vendor.pk)
            vendor.credit += self.amount
            vendor.save()
            credit_request.save()
            TransactionLog.objects.create(
                vendor=self.vendor,
                amount=self.amount,
                transaction_type=TransactionLog.CREDIT_INCREASE
            )


class TransactionLog(BaseModel):
    CREDIT_INCREASE = 'credit_increase'
    CREDIT_DECREASE = 'credit_decrease'
    TOPUP = 'topup'

    TRANSACTION_TYPES = [
        (CREDIT_INCREASE, 'Credit Increase'),
        (CREDIT_DECREASE, 'Credit Decrease'),
        (TOPUP, 'TopUp'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)