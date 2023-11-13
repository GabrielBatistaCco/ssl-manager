from django.db import models

class StatusSSL(models.TextChoices):
    VAZIO = None , '-'
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    VENCIDO = 'Vencido'
    ABANDONADO = 'Abandonado'

class Cert (models.Model):
    id = models.AutoField(primary_key=True)
    dominio = models.CharField(verbose_name="Domínio", max_length=100)
    url_ssls = models.CharField(verbose_name="URL ssls", null=True, max_length=100)
    validade_ssl = models.DateField(verbose_name="Validade certificado", null=True)
    criado_em = models.DateTimeField(verbose_name="Data cadastro", auto_now_add=True, null=False, blank=False)
    issuer = models.CharField(verbose_name="Organização", null=True, max_length=100)
    status_ssl = models.CharField(
        max_length=10,
        choices=StatusSSL.choices,
        verbose_name='Status SSL',
        default=None
    )
