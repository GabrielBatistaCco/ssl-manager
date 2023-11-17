from django.db import models
from rest_framework.exceptions import ValidationError
from django.core.validators import URLValidator

class Cert (models.Model):

    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
        ('Vencido', 'Vencido'),
        ('Abandonado', 'Abandonado'),
        ('Último dia', 'Último dia'),
        ('Disponível', 'Disponível')
    ]

    id = models.AutoField(primary_key=True)
    dominio = models.CharField(
        verbose_name="Domínio", 
        null=False,
        blank=False,
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
        choices=STATUS_CHOICES,
        verbose_name='Status SSL',
        null=True,
        blank=False,
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

        if self.url_ssls:
            if Cert.objects.filter(dominio=self.dominio).exclude(pk=self.pk).exists():
                raise ValidationError({'dominio': self.field.error_messages['unique']})

            # if not (self.url_ssls.startswith('http://') or self.url_ssls.startswith('https://')):
            #     self.url_ssls = f'https://{self.url_ssls}'

            url_validator = URLValidator(schemes=['http', 'https'])
            try:
                url_validator(self.url_ssls)
            except ValidationError:
                raise ValidationError({'url_ssls': 'A URL deve ter o formato correto (por exemplo, "https://www.exemplo.com")'})

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e:
            raise ValidationError(detail=e.message_dict)

        super().save(*args, **kwargs)
