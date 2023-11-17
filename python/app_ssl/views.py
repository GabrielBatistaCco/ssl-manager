# from django.urls import reverse, reverse_lazy
# from django.http import HttpResponseRedirect
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Cert
from .get_ssl import GetSSLCert
from django.shortcuts import render
# , get_object_or_404, redirect
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import CertSerializer
import pandas as pd
import asyncio

class CertViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def perform_create(self, serializer):
        dominio = serializer.validated_data.get('dominio')

        get_ssl = GetSSLCert(dominio)

        resultado_validade = get_ssl.get_validade_ssl()
        resultado_status = get_ssl.get_status_ssl()
        serializer.validated_data.update(resultado_validade)
        serializer.validated_data.update(resultado_status)

        serializer.save()

    def perform_update(self, serializer):
        dominio = serializer.validated_data.get('dominio')

        get_ssl = GetSSLCert(dominio)

        resultado_validade = get_ssl.get_validade_ssl()
        resultado_status = get_ssl.get_status_ssl()
        serializer.validated_data.update(resultado_validade)
        serializer.validated_data.update(resultado_status)

        serializer.save()
    
class CsvViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()

    @action(detail=False, methods=['POST'])
    def importar_csv(self, request):
        if 'arquivo' not in request.FILES:
            return Response({'detail': 'O arquivo não foi fornecido'}, status=400)

        arquivo_csv = request.FILES['arquivo']

        try:
            dados_csv = pd.read_csv(arquivo_csv)
            dados_filtrados = dados_csv[
                (dados_csv['details_URL'].notna()) &
                (dados_csv['status'].isin(['ISSUED', 'PAUSED', 'UNUSED']))
            ]
            campos_modelo = Cert._meta.get_fields()

            for index, linha in dados_filtrados.iterrows():
                csv_dominio = linha.get('common_name')
                csv_validade_ssl = linha.get('expire_date')
                csv_status_ssl = linha.get('status')

                get_ssl = GetSSLCert(csv_dominio, status_ssl=csv_status_ssl, validade_ssl=csv_validade_ssl)
                get_status_ssl = get_ssl.get_status_ssl()
                
                status_ssl = get_status_ssl['status_ssl']
                dominio = get_status_ssl['dominio'] if 'dominio' in get_status_ssl else csv_dominio
                validade_ssl = get_status_ssl['validade_ssl'] if 'validade_ssl' in get_status_ssl else csv_validade_ssl

                valores_campos = {
                    'dominio': dominio,
                    'url_ssls': linha.get('details_URL'),
                    'validade_ssl': validade_ssl,
                    'issuer': linha.get('type'),
                    'status_ssl': status_ssl
                }

                print(valores_campos)

                cert_instance, index = Cert.objects.get_or_create(dominio=csv_dominio)

                for campo, valor in valores_campos.items():
                    setattr(cert_instance, campo, valor)

                cert_instance.save()

            return Response({'detail': 'Dados importados com sucesso'}, status=200)

        except pd.errors.EmptyDataError:
            return Response({'detail': 'O arquivo CSV está vazio'}, status=400)

        except pd.errors.ParserError:
            return Response({'detail': 'Erro ao analisar o arquivo CSV'}, status=400)
