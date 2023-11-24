from django.contrib import admin
from django.urls import path, include
from app_ssl.views import CertViewSet, CsvViewSet, RefreshCertsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'certificates', CertViewSet, basename='certificates')
router.register(r'import_csv', CsvViewSet, basename='import_csv')
router.register(r'refresh_certificates', RefreshCertsViewSet, basename='refresh_certificates')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]