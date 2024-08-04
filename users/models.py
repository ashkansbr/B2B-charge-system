import decimal
import logging
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.exceptions import ValidationError
from common.basemodel import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Vendor(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=10, decimal_places=2)

    def adjust_credit(self, amount):
        with transaction.atomic():
            vendor = Vendor.objects.select_for_update().get(pk=self.pk)
            if vendor.credit + amount < 0:
                raise ValidationError("Insufficient credit")
            vendor.credit += decimal.Decimal(amount)
            vendor.save()

    def __str__(self):
        return f"Vendor: {self.user.username} - Credit: {self.credit}"


class PhoneNumber(BaseModel):

    number = models.CharField(max_length=15, unique=True)
    total_amount_added = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.number
