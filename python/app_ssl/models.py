from django.db import models

class Certificado (models.Model):
    id = models.AutoField(primary_key=True)
    dominio = models.TextField(max_length=255)
    url_ssls = models.TextField(max_length=255)
    # status_ssl = models.TextChoices("ativo","vencido","renovar")     Analisar mais status possíveis
    # status_cadstro = models.TextChoices("ok","imcompleto","inconsistente")    Para alertar cadastros que precisam ser revisados
    # tipo = models.TextChoices("ssls", "letsencrypt")   Talvez pegar a certificadora na consulta do SSL
    validade = models.DateField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=False, blank=False)
