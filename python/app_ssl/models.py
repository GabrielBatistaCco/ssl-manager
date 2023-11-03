from django.db import models

class Cert (models.Model):
    id = models.AutoField(primary_key=True)
    dominio = models.CharField(verbose_name="Domínio", max_length=100)
    url_ssls = models.CharField(verbose_name="URL ssls", null=True, max_length=100)
    # status_ssl = models.TextChoices("ativo","vencido","renovar")     Analisar mais status possíveis
    # status_cadstro = models.TextChoices("ok","imcompleto","inconsistente")    Para alertar cadastros que precisam ser revisados
    # tipo = models.TextChoices("ssls", "letsencrypt")   Talvez pegar a certificadora na consulta do SSL
    validade = models.DateField(verbose_name="Validade certificado", null=True)
    criado_em = models.DateTimeField(verbose_name="Data cadastro", auto_now_add=True, null=False, blank=False)
