from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, VendorViewSet, PhoneNumberViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'phonenumbers', PhoneNumberViewSet, basename='phonenumber')


urlpatterns = [
    path('', include(router.urls)),
]
