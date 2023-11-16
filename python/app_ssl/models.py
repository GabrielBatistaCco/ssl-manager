from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class StatusSSL(models.TextChoices):
    VAZIO = None , '-'
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    VENCIDO = 'Vencido'
    ABANDONADO = 'Abandonado'

class Cert (models.Model):
    id = models.AutoField(primary_key=True)
    dominio = models.CharField(
        verbose_name="Domínio", 
        null=False, 
        unique=True, 
        error_messages={
            'unique': 'Este domínio já está cadastrado.',
        },
        max_length=100
    )
    url_ssls = models.CharField(
        verbose_name="URL ssls", 
        null=True, 
        max_length=100
    )
    validade_ssl = models.DateField(
        verbose_name="Validade certificado", 
        null=True
    )
    issuer = models.CharField(
        verbose_name="Emissor", 
        null=True, 
        max_length=100
    )
    status_ssl = models.CharField(
        max_length=10,
        choices=StatusSSL.choices,
        verbose_name='Status SSL',
        null=True,
    )
    criado_em = models.DateTimeField(
        verbose_name="Data cadastro", 
        auto_now_add=True, 
        null=False, 
        blank=False
    )

    def clean(self):
        super().clean()

        if self.url_ssls:
            if Cert.objects.filter(dominio=self.dominio).exclude(pk=self.pk).exists():
                raise ValidationError({'dominio': self.field.error_messages['unique']})

            if not (self.url_ssls.startswith('http://') or self.url_ssls.startswith('https://')):
                self.url_ssls = f'https://{self.url_ssls}'

            url_validator = URLValidator(schemes=['http', 'https'])
            try:
                url_validator(self.url_ssls)
            except ValidationError:
                raise ValidationError({'url_ssls': 'A URL deve ter o formato correto (por exemplo, "https://www.exemplo.com")'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
