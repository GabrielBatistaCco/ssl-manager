from django.contrib import admin
from django.urls import path, include
from app_ssl.controller import CertViewSet, CsvViewSet, RefreshCertsViewSet, AuditLogView, AuthUserView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'certificates', CertViewSet, basename='certificates')
router.register(r'import_csv', CsvViewSet, basename='import_csv')
router.register(r'refresh_certificates', RefreshCertsViewSet, basename='refresh_certificates')
router.register(r'audit', AuditLogView, basename='audit')
router.register(r'auth_user', AuthUserView, basename='auth_user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
