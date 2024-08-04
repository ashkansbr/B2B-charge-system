from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditRequestViewSet, TransactionLogViewSet

router = DefaultRouter()
router.register(r'credit_requests', CreditRequestViewSet)
router.register(r'transaction_logs', TransactionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
