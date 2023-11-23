from django.db import models

class Cert(models.Model):
    dominio = models.CharField(
        verbose_name="Domínio", 
        null=True,
        blank=True,
        max_length=100
    )
    url_ssls = models.CharField(
        verbose_name="URL ssls", 
        null=True,
        blank=True,
        max_length=100
    )
    ativacao_ssl = models.DateField(
        verbose_name="Data início certificado",
        null=True,
        blank=True
    )
    validade_ssl = models.DateField(
        verbose_name="Data fim certificado",
        null=True,
        blank=True
    )
    emissor = models.CharField(
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
            ('Disponível', 'Disponível'),
            ('Inconsistente','Inconsistente')
        ],
        verbose_name='Status SSL',
        null=False,
        blank=True,
        max_length=13
    )
    criado_em = models.DateTimeField(
        verbose_name="Data cadastro", 
        auto_now_add=True, 
        null=False,
        blank=False
    )
