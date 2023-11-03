from django.contrib import admin
from django.urls import path
from app_ssl import views

urlpatterns = [
    # path('', views.listar_ssl, name='listar_ssl'),
    path("admin/", admin.site.urls),
    path("", views.CertListView.as_view(), name='lista_ssl'),
    path('cadastro_ssl/', views.CertCreateView.as_view(), name='cadastro_ssl'),
    path('editar_ssl/<int:pk>', views.CertUpdateView.as_view(), name='editar_ssl'),
    path('excluir_ssl/<int:pk>', views.CertDeleteView.as_view(), name='excluir_ssl'),
]
