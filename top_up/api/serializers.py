from rest_framework import serializers
from ..models import TopUp
from users.models import PhoneNumber


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'number', 'total_amount_added']
        read_only_fields = ['id', 'total_amount_added']


class TopUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = TopUp
        fields = ['id', 'vendor', 'phone_number', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at', 'vendor']

    def create(self, validated_data):
        phone_number_str = validated_data.pop('phone_number')
        phone_number, created = PhoneNumber.objects.get_or_create(number=phone_number_str)
        top_up = TopUp.objects.create(phone_number=phone_number, **validated_data)
        return top_up
