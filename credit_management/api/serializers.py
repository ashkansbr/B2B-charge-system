from rest_framework import serializers
from ..models import CreditRequest, TransactionLog
from django.core.exceptions import ValidationError


class CreditRequestSerializer(serializers.ModelSerializer):

    is_approved = serializers.BooleanField(read_only=True)
    vendor = serializers.ReadOnlyField(source='vendor.id')

    class Meta:
        model = CreditRequest
        fields = ['id', 'vendor', 'amount', 'is_approved', 'created_at', 'approved_at']
        read_only_fields = ['approved_at',]

    def update(self, instance, validated_data):
        if 'is_approved' in validated_data:
            if validated_data['is_approved'] and not instance.is_approved:
                try:
                    instance.approve()
                except ValidationError as e:
                    raise serializers.ValidationError(e.messages)
        return super().update(instance, validated_data)


class CreditRequestApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ['is_approved']


class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = ['id', 'vendor', 'amount', 'transaction_type', 'created_at']
