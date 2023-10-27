from django.urls import path
from app_ssl import views

urlpatterns = [
    path('', views.listar_ssl, name='listar_ssl'),
    path('insere_ssl/', views.insere_ssl, name='insere_ssl'),
    path('cadastrar_ssl/', views.cadastrar_ssl, name='cadastrar_ssl'),
    path('deletar_ssl/', views.deletar_ssl, name='deletar_ssl'),
    
]
