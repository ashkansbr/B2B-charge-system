from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import CreditRequest, TransactionLog
from .serializers import CreditRequestSerializer, TransactionLogSerializer, CreditRequestApprovalSerializer
from rest_framework.permissions import IsAdminUser
from users.models import Vendor


class CreditRequestViewSet(viewsets.ModelViewSet):
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer

    def perform_create(self, serializer):
        vendor = Vendor.objects.get(user=self.request.user)
        serializer.save(vendor=vendor)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        credit_request = self.get_object()
        try:
            credit_request.approve()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreditRequestApprovalSerializer(credit_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer
