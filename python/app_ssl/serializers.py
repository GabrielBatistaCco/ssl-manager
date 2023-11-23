from rest_framework import serializers
from .models import Cert
import re

class CertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cert
        fields = (
         'id',
         'dominio', 
         'url_ssls', 
        )

    def to_representation(self, instance):
        if isinstance(instance, dict):
            # Tratar caso seja um OrderedDict (lista de objetos)
            return instance

        representation = super().to_representation(instance)
        representation['ativacao_ssl'] = instance.ativacao_ssl
        representation['validade_ssl'] = instance.validade_ssl
        representation['emissor'] = instance.emissor
        representation['status_ssl'] = instance.status_ssl

        return representation

    def validate_data(self, data):
        dominio = data.get('dominio')
        url_ssls = data.get('url_ssls') # https://www.ssls.com/user/bundles/view/...

        dominio_exists = Cert.objects.filter(dominio=dominio).exclude(pk=self.instance.pk if self.instance else None).exists() if dominio is not None else False
        url_exists = Cert.objects.filter(url_ssls=url_ssls).exclude(pk=self.instance.pk if self.instance else None).exists() if url_ssls is not None else False

        url_validator = re.compile(r'^(http|https)://(www\.)?ssls\.com/user/bundles/view/[a-zA-Z0-9]+$')

        if dominio_exists:
            raise serializers.ValidationError(f'Este domínio já está cadastrado, verifique a lista de certificados.')
        elif url_ssls is not None and not url_validator.match(url_ssls):
            raise serializers.ValidationError('URL inválida, deve estar no formato "https://www.ssls.com/user/bundles/view/..."')
        elif url_exists:
            raise serializers.ValidationError('Esta URL já está cadastrada, verifique a lista de certificados.')

        return data

    def create(self, validated_data):
        return Cert.objects.create(**validated_data)