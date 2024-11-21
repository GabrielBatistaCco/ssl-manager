from app_ssl.models import Cert, AuditLog
from app_ssl.utils.get_ssl import GetSSLCert
from app_ssl.utils.import_csv import GetCSVCerts
from app_ssl.utils.serializers import CertSerializer, AuditLogSerializer
from app_ssl.utils.task_locker import TaskLocker
from app_ssl.utils.certificate_utils import RefreshCertificates
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from django.db.models import Q
from django.shortcuts import redirect
import json
import jwt
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
import pandas as pd
import random
import string
import requests
import uuid

class CertViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer
    task_locker = TaskLocker()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values(
            'id',
            'product_id',
            'domain',
            # 'activation_ssl',
            'expiration_ssl',
            'product_name',
            'issuer',
            'status_ssl',
        )

        return Response(list(queryset), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_cert_operation(serializer)

        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'detail': 'success', 'data': serializer.data }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_cert_operation(serializer, is_update=True)
        self.unlock()
        
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({ 'detail': 'success', 'data': serializer.data }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response({'detail': 'success'}, status=status.HTTP_200_OK)
        except Cert.DoesNotExist:
            raise ValidationError({'detail': 'not_found'}, code=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        task_name = str(f'cert_{instance.pk}')

        def callback():
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return self.task_locker.lock_task(task_name, callback, delay_seconds=3600, data=True) # dalay = 1h

    def perform_cert_operation(self, serializer, is_update=False):
        domain_form = serializer.validated_data.get('domain')
        ssls_url_form = serializer.validated_data.get('ssls_url')
        product_name_form = serializer.validated_data.get('product_name')
        email_form = serializer.validated_data.get('email')
        pk = serializer.instance.pk if serializer.instance else None

        get_ssl = GetSSLCert({
            "domain": domain_form,
            "ssls_url": ssls_url_form,
            "email": email_form,
            "pk": pk,
        })

        data_to_validate = {
            "domain": get_ssl.domain,
            "ssls_url": get_ssl.ssls_url,
            "product_name": product_name_form,
            "email": email_form,
        }
        serializer.validate_data(data_to_validate)

        try:
            certificate_data = get_ssl.get_certificate()
            serializer.validated_data.update(certificate_data, user='User')

            serializer.save()

        except Exception as e:
            return Response({'detail': 'cert_error'}, status=status.HTTP_200_OK)
            # return Response({'detail': e}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='unlock')
    def unlock(self, *args, **kwargs):
        instance = self.get_object()
        task_name = str(f'cert_{instance.pk}')
        self.task_locker._delay_and_delete_cache(task_name, delay_seconds=0)

        return Response({'detail': 'success'})

class CsvViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer
    task_locker = TaskLocker()

    def create(self, request, *args, **kwargs):
        task_name = "change_certs"

        def callback():
            if 'file' not in request.FILES:
                return Response({'detail': 'not_found'}, status=status.HTTP_200_OK)

            csv_file = request.FILES['file']
            csv_certs_instance = GetCSVCerts()
            
            return csv_certs_instance.import_csv(csv_file)

        return self.task_locker.lock_task(task_name, callback, delay_seconds=0)

class RefreshCertsViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer
    task_locker = TaskLocker()

    def list(self, request, *args, **kwargs):
        task_name = "change_certs"

        def callback():
            # certs_to_refresh = Cert.objects.only('id', 'domain', 'ssls_url', 'email').values()
            return RefreshCertificates.refresh_certificates(self.queryset.values())

        return self.task_locker.lock_task(task_name, callback, delay_seconds=0)

class AuditLogView(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    @action(detail=True, methods=['get'])
    def record_logs(self, request, pk=None):
        try:
            audit_logs = AuditLog.objects.filter(record_id=pk).order_by('-timestamp')
            serializer = self.get_serializer(audit_logs, many=True)
            return Response({'audit_logs': serializer.data})
        except AuditLog.DoesNotExist:
            return Response({'detail': 'not_found'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def detailed_logs(self, request, pk=None):
        try:
            cert = Cert.objects.get(pk=pk)
            domain = cert.domain
            ssls_url = cert.ssls_url
            
            if not domain:
                audit_logs = AuditLog.objects.filter(Q(cert_data__icontains=ssls_url)).order_by('-timestamp')
            elif not ssls_url:
                audit_logs = AuditLog.objects.filter(Q(cert_data__icontains=domain)).order_by('-timestamp')
            else:
                audit_logs = AuditLog.objects.filter(Q(cert_data__icontains=domain) | Q(cert_data__icontains=ssls_url)).order_by('-timestamp')
            
            serializer = AuditLogSerializer(audit_logs, many=True)
            return Response({'audit_logs': serializer.data})
        except AuditLog.DoesNotExist:
            return Response({'detail': 'not_found'}, status=status.HTTP_200_OK)


class AuthUserView(viewsets.ModelViewSet):
    # ... (outros métodos)

    @action(detail=False, methods=['get'], url_path='generate_hash')
    def generate_hash():
        random_hash = str(uuid.uuid4()).replace('-', '')[:32]
        #print(f'Hash gerada: {random_hash}')  # Imprime a hash no terminal (remova em produção)
        return Response({'hash': random_hash}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='login')  
    def login(self, request):
        random_hash = AuthUserView.generate_hash()
        redirect_uri = 'https://papaya.ixcsoft.com.br:8000/auth_user/process_keycloak_token/'
        client_id = 'certificadossl.ixcsoft.com.br'
        keycloak_url = f"https://sso.ixcsoft.com.br/realms/ixcsoft/protocol/openid-connect/auth?state={random_hash}&scope=profile%20email&response_type=code&approval_prompt=auto&redirect_uri={redirect_uri}&client_id={client_id}"
        return Response({"redirectURL": keycloak_url}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='process_keycloak_token')
    def process_keycloak_token(self, request):
        tela_inicial = 'https://papaya.ixcsoft.com.br/ssl'
        try:
            code = request.GET.get('code')

            client_id = 'certificadossl.ixcsoft.com.br'
            client_secret = 'TffYaVxrGp09pTplXXcuKEexsO12v0MY'
            redirect_uri = 'https://papaya.ixcsoft.com.br:8000/auth_user/process_keycloak_token/'  # Altere conforme necessário
            
            keycloak_token_url = 'https://sso.ixcsoft.com.br/realms/ixcsoft/protocol/openid-connect/token/'
            keycloak_token_data = {
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': redirect_uri,
            }

            keycloak_token_response = requests.post(keycloak_token_url, data=keycloak_token_data)

            print(keycloak_token_response.json())

            if keycloak_token_response.status_code == 200:
                keycloak_token_data = keycloak_token_response.json()

                if 'access_token' in keycloak_token_data:
                    token_de_sessao = keycloak_token_data['access_token']

                    decoded_payload = jwt.decode(token_de_sessao, options={"verify_signature": False})
                    print("Token decodificado com sucesso:")
                    print(decoded_payload)

                    if decoded_payload:
                        nome_do_usuario = decoded_payload.get('name')
                        email_do_usuario = decoded_payload.get('email')

                        # Execute lógica de auditoria aqui, usando token_de_sessao e nome_do_usuario
                        # ...

                        # Redirecione para a página desejada após o login
                        return redirect(f'{tela_inicial}',status=status.HTTP_200_OK)
                        

                    else:
                        return Response({"error": "Erro ao decodificar o token JWT"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "O campo 'access_token' não está presente na resposta do Keycloak"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Erro ao obter o token do Keycloak"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='handle_login_redirect')
    def handle_login_redirect(self, request):
        # Esta rota será chamada pelo frontend para obter os dados e redirecionar corretamente
        nome_do_usuario = request.GET.get('name', '')
        email_do_usuario = request.GET.get('email', '')

        return Response({"name": nome_do_usuario, "email": email_do_usuario}, status=status.HTTP_200_OK)
