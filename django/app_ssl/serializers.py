from rest_framework import serializers
from .models import Cert
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
        ssls_url = data.get('ssls_url')  # https://www.ssls.com/user/bundles/view/...

        domain_exists = Cert.objects.filter(domain=domain).exclude(pk=self.instance.pk if self.instance else None).exists() if domain is not None else False
        url_exists = Cert.objects.filter(ssls_url=ssls_url).exclude(pk=self.instance.pk if self.instance else None).exists() if ssls_url is not None else False

        url_validator = re.compile(r'^(http|https)://(www\.)?ssls\.com/user/bundles/view/[a-zA-Z0-9]+$')

        if domain_exists:
            raise serializers.ValidationError(f'This domain is already registered, check the list of certificates.')
        elif ssls_url is not None and not url_validator.match(ssls_url):
            raise serializers.ValidationError('Invalid URL, must be in the format "https://www.ssls.com/user/bundles/view/..."')
        elif url_exists:
            raise serializers.ValidationError('This URL is already registered, check the list of certificates.')

        return data

    def create(self, validated_data):
        return Cert.objects.create(**validated_data)
