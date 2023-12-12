from .models import Cert
from .custom_errors import CustomValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
import re

class CertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cert
        fields = (
         'id',
         'domain', 
         'ssls_url', 
         'product_name', 
        )

    def to_representation(self, instance):
        if isinstance(instance, dict):
            # Handle case where it's an OrderedDict (list of objects)
            return instance

        representation = super().to_representation(instance)
        representation['activation_ssl'] = instance.activation_ssl
        representation['expiration_ssl'] = instance.expiration_ssl
        representation['activation_weekday'] = instance.activation_weekday
        representation['expiration_weekday'] = instance.expiration_weekday
        representation['issuer'] = instance.issuer
        representation['status_ssl'] = instance.status_ssl

        return representation

    def validate_data(self, data):
        domain = data.get('domain') 
        ssls_url = data.get('ssls_url') # https://www.ssls.com/user/bundles/view/...
        product_name = data.get('product_name')

        ssls_url_regex = re.compile(r'^(http|https)://(www\.)?ssls\.com/user/bundles/view/[a-zA-Z0-9]+$')
        ssls_url_validator = ssls_url_regex.match(ssls_url) if ssls_url is not None else True

        domain_exists = Cert.objects.filter(domain=domain).exclude(pk=self.instance.pk if self.instance else None).exists() if domain is not None else False
        url_exists = Cert.objects.filter(ssls_url=ssls_url).exclude(pk=self.instance.pk if self.instance else None).exists() if ssls_url is not None else False

        if not product_name:
            raise CustomValidationError('A product must be filled in!', status_code=status.HTTP_200_OK)

        if not domain and not ssls_url:
            raise CustomValidationError('At least one of the fields "Domain" or "SSL URL" must be filled.', status_code=status.HTTP_200_OK)

        if not ssls_url_validator:
            raise CustomValidationError('Invalid URL, must be in the format "https://www.ssls.com/user/bundles/view/..."', status_code=status.HTTP_200_OK)
        
        if domain_exists:
            raise CustomValidationError('This domain is already registered, check the list of certificates.', status_code=status.HTTP_200_OK)

        if url_exists:
            raise CustomValidationError('This URL is already registered, check the list of certificates.', status_code=status.HTTP_200_OK)

        return data

    def create(self, validated_data):
        return Cert.objects.create(**validated_data)
