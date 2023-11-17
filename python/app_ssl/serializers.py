from rest_framework import serializers
from .models import Cert

class CertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cert
        fields = (
         'id',
         'dominio', 
         'url_ssls', 
         'validade_ssl', 
         'status_ssl',
         'issuer'
        )

    def create(self, validated_data):
        return Cert.objects.create(**validated_data)