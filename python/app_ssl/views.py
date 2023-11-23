from .models import Cert
from .get_ssl import GetSSLCert
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import viewsets, status
from .serializers import CertSerializer
import pandas as pd

class CertViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def perform_cert_operation(self, serializer, is_update=False):

        form_dominio = serializer.validated_data.get('dominio')
        form_url_ssls = serializer.validated_data.get('url_ssls')

        if not form_dominio and not form_url_ssls:
            raise ValidationError({'detail': 'Pelo menos um dos campos "Domínio" ou "URL ssls" deve ser preenchido.'})

        get_ssl = GetSSLCert(dominio=form_dominio, url_ssls=form_url_ssls)

        # Valida dominio e url_ssls
        data_to_validate = {"dominio": get_ssl.dominio, "url_ssls": get_ssl.url_ssls}
        serializer.validate_data(data_to_validate)

        try:
            # import pdb; pdb.set_trace()
            dados_certificado = get_ssl.get_certificado(datas=True, status=True)
            serializer.validated_data.update(dados_certificado)

            serializer.save()

        except Exception as e:
            return Response({'detail': f'Erro ao obter o certificado: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_cert_operation(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_cert_operation(serializer, is_update=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response({'detail': 'Registro excluído com sucesso.'}, status=status.HTTP_200_OK)
        except Cert.DoesNotExist:
            raise ValidationError({'detail': 'Registro não encontrado.'})

class CsvViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    @action(detail=False, methods=['POST'])
    def importar_csv(self, request):
        if 'arquivo' not in request.FILES:
            return Response({'detail': 'O arquivo não foi fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        arquivo_csv = request.FILES['arquivo']

        try:
            dados_csv = pd.read_csv(arquivo_csv)
            dados_filtrados = self.filtrar_dados_csv(dados_csv)

            for index, linha in dados_filtrados.iterrows():
                self.processar_linha_csv(linha)

            return Response({'detail': 'Dados importados com sucesso'}, status=status.HTTP_200_OK)

        except pd.errors.EmptyDataError:
            return Response({'detail': 'O arquivo CSV está vazio'}, status=status.HTTP_400_BAD_REQUEST)

        except pd.errors.ParserError:
            return Response({'detail': 'Erro ao analisar o arquivo CSV'}, status=status.HTTP_400_BAD_REQUEST)

    def filtrar_dados_csv(self, dados_csv):
        return dados_csv[
            (dados_csv['details_URL'].notna()) &
            (dados_csv['status'].isin(['ISSUED', 'PAUSED', 'UNUSED'])) &
            (~dados_csv['common_name'].astype(str).str.startswith('*'))
        ]

    def processar_linha_csv(self, linha):
        csv_dominio = linha.get('common_name')
        csv_url_ssls = linha.get('details_URL')

        get_ssl = GetSSLCert(
            dominio=csv_dominio,
            url_ssls=csv_url_ssls
        )

        dados_certificado = get_ssl.get_certificado(datas=False, status=True)

        csv_cert, index = Cert.objects.get_or_create(dominio=csv_dominio)

        for campo, valor in dados_certificado.items():
            setattr(csv_cert, campo, valor)

        print(dados_certificado)
        csv_cert.save()
