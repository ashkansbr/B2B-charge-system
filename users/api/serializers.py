from rest_framework import serializers
from ..models import CustomUser, Vendor, PhoneNumber
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class VendorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    vendor_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Vendor
        fields = ['id', 'vendor_id', 'user', 'credit']


class VendorCreditSerializer(serializers.ModelSerializer):
    vendor = serializers.ReadOnlyField(source='vendor.id')

    class Meta:
        model = Vendor
        fields = ['vendor', 'credit']


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'number','total_amount_added', 'created_at']