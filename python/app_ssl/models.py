from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models

class Cert (models.Model):

    id = models.AutoField(primary_key=True)
    dominio = models.CharField(
        verbose_name="Domínio", 
        null=True,
        blank=True,
        unique=True,
        error_messages={
            'unique': 'Este domínio já está cadastrado.',
        },
        max_length=100
    )
    url_ssls = models.CharField(
        verbose_name="URL ssls", 
        null=True,
        blank=True,
        max_length=100
    )
    validade_ssl = models.DateField(
        verbose_name="Validade certificado",
        null=True,
        blank=True
    )
    issuer = models.CharField(
        verbose_name="Emissor",
        null=True,
        blank=True,
        max_length=100
    )
    status_ssl = models.CharField(
        choices=[
            ('Ativo', 'Ativo'),
            ('Inativo', 'Inativo'),
            ('Vencido', 'Vencido'),
            ('Abandonado', 'Abandonado'),
            ('Último dia', 'Último dia'),
            ('Disponível', 'Disponível')
        ],
        verbose_name='Status SSL',
        null=True,
        blank=True,
        max_length=10
    )
    criado_em = models.DateTimeField(
        verbose_name="Data cadastro", 
        auto_now_add=True, 
        null=False,
        blank=False
    )

    def clean(self):
        super().clean()

        if self.dominio and Cert.objects.filter(dominio=self.dominio).exclude(pk=self.pk).exists():
            raise DRFValidationError({'dominio': f'O domínio "{self.dominio}" já está cadastrado.'})

        if self.url_ssls:
            url_validator = URLValidator(schemes=['http', 'https'])
            try:
                url_validator(self.url_ssls)
            except ValidationError:
                raise DRFValidationError({'url_ssls': 'A URL deve ter o formato correto (por exemplo, "https://www.exemplo.com")'})

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except DRFValidationError as e:
            raise e

        super().save(*args, **kwargs)
