from app_ssl.models import Cert, AuditLog, EmailQueue
from app_ssl.utils.custom_errors import CustomValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
# from validate_email_address import validate_email
import re
import traceback

class CertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cert
        fields = ('id', 'domain', 'ssls_url', 'product_name', 'notes', 'email')

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance

        representation = super().to_representation(instance)
        representation['activation_ssl'] = instance.activation_ssl
        representation['expiration_ssl'] = instance.expiration_ssl
        representation['activation_weekday'] = instance.activation_weekday
        representation['expiration_weekday'] = instance.expiration_weekday
        representation['issuer'] = instance.issuer
        representation['status_ssl'] = instance.status_ssl
        representation['product_id'] = instance.product_id

        return representation

    def validate_data(self, data):
        self.pk=self.instance.pk if self.instance else None
        self.domain = data.get('domain')
        self.ssls_url = data.get('ssls_url')
        self.product_name = data.get('product_name')
        self.email = data.get('email')

        domain_regex = r'^(http|https)://(www\.)?ssls\.com/user/bundles/view/[a-zA-Z0-9]+$'
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            # https://www.ssls.com/user/bundles/view/...
            ssls_url_match = re.match(domain_regex, self.ssls_url)
        except TypeError:
            ssls_url_match = True
        except Exception as e:
            print(f'Serializer [ssls_url_match]: {e}')

        domain_exists = Cert.objects.filter(
            domain=self.domain,
            domain__isnull=False,
        ).exclude(pk=self.pk).first() if self.domain is not None else False

        ssls_url_exists = Cert.objects.filter(
            ssls_url=self.ssls_url,
            ssls_url__isnull=False,
        ).exclude(pk=self.pk).first() if self.ssls_url is not None else False

        if not self.product_name:
            # Produto vazio
            raise CustomValidationError('product_empty', status_code=status.HTTP_200_OK)

        if not self.domain and not self.ssls_url:
            # Dominio E url vazios
            raise CustomValidationError('cert_empty', status_code=status.HTTP_200_OK)

        if domain_exists:
            # Domínio já existe
            raise CustomValidationError('domain_exists', status_code=status.HTTP_200_OK)

        if self.ssls_url and not ssls_url_match:
            # url inválida
            raise CustomValidationError('invalid_url', status_code=status.HTTP_200_OK)

        if ssls_url_exists:
            # url já existe
            raise CustomValidationError('url_exists', status_code=status.HTTP_200_OK)

        if self.email is not None and not re.match(email_regex, self.email):
            # Formato de email incorreto
            raise CustomValidationError('invalid_email', status_code=status.HTTP_200_OK)

        return data

    def create(self, validated_data):
        return Cert.objects.create(**validated_data)

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class EmailQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailQueue
        fields = '__all__'