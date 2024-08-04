from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopUpViewSet

router = DefaultRouter()
router.register(r'topups', TopUpViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
