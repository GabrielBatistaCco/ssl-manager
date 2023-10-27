from django.db import models

class Certificado (models.Model):
    id_ssl = models.AutoField(primary_key=True)
    dominio = models.TextField(max_length=255)

