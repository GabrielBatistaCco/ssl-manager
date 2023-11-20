from django.contrib import admin
from django.urls import path, include
from app_ssl.views import CertViewSet, CsvViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'certificados', CertViewSet, basename='certificados')
router.register(r'csv', CsvViewSet, basename='csv')

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
