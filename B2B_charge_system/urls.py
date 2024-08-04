from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from common.swaggers import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.api.urls')),
    path('api/credit_management/', include('credit_management.api.urls')),
    path('api/top_up/', include('top_up.api.urls')),
    # path('Token/', TokenObtainPairView.as_view()),
    # path('Token/refresh/', TokenRefreshView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
