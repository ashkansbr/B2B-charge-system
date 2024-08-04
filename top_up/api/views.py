from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from ..models import TopUp
from .serializers import TopUpSerializer


class TopUpViewSet(viewsets.ModelViewSet):
    queryset = TopUp.objects.all()
    serializer_class = TopUpSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(vendor=self.request.user.vendor)
        except DjangoValidationError as e:
            raise DRFValidationError({"detail": e.messages})
