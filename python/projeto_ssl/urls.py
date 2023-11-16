from django.contrib import admin
from django.urls import path, include
# from app_ssl import views
from app_ssl.views import CertViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'certificados', CertViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path("", views.CertListView.as_view(), name='lista_ssl'),
    # path('cadastrar_ssl/', views.CertCreateView.as_view(), name='cadastrar_ssl'),
    # path('editar_ssl/<int:pk>/', views.CertUpdateView.as_view(), name='editar_ssl'),
    # path('excluir_ssl/<int:pk>/', views.CertDeleteView.as_view(), name='excluir_ssl'),
]
