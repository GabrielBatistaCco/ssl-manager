from django.shortcuts import render, redirect
from .models import Certificado

def cadastrar_ssl(request):
    return render(request, 'ssl/cadastro_ssl.html')

def listar_ssl(request):
    # Consultar certificados cadastrados em uma nova página
    certificados = {
        'certificados': Certificado.objects.all()
    }
    # Retornar certificados para página de listagem
    return render(request, 'ssl/lista_ssl.html', certificados)

def insere_ssl(request):
    if request.method == 'POST':
        # Salvar os dados da tela no banco de dados
        novo_ssl = Certificado()
        novo_ssl.dominio = request.POST.get('dominio')
        novo_ssl.url_ssls = request.POST.get('url_ssls')
        novo_ssl.save()

    return redirect('listar_ssl')

def deletar_ssl(request):
    if request.method == "DELETE":
        deletar_ssl = Certificado()
        deletar_ssl.id_ssl = request.DELETE.getlist('ids_ssl')
        deletar_ssl.save()