from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from ..models import CustomUser, Vendor, PhoneNumber
from .serializers import CustomUserSerializer, VendorSerializer, VendorCreditSerializer, PhoneNumberSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return VendorSerializer
        return VendorCreditSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
