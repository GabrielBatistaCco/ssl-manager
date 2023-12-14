from django.db import models

class Cert(models.Model):
    domain = models.CharField(
        verbose_name="Domain", 
        null=True,
        blank=True,
        max_length=100
    )
    ssls_url = models.CharField(
        verbose_name="SSL URL", 
        null=True,
        blank=True,
        max_length=100
    )
    activation_ssl = models.DateField(
        verbose_name="Certificate start date",
        null=True,
        blank=True
    )
    expiration_ssl = models.DateField(
        verbose_name="Certificate end date",
        null=True,
        blank=True
    )
    activation_weekday = models.CharField(
        verbose_name="Activation day", 
        null=True,
        blank=True,
        max_length=100
    )
    expiration_weekday = models.CharField(
        verbose_name="Expiration day", 
        null=True,
        blank=True,
        max_length=100
    )
    issuer = models.CharField(
        verbose_name="Issuer",
        null=True,
        blank=True,
        max_length=100
    )
    status_ssl = models.CharField(
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
            ('Expired', 'Expired'),
            ('Abandoned', 'Abandoned'),
            ('Last day', 'Last day'),
            ('Last week', 'Last week'),
            ('Last month', 'Last month'),
            ('Available', 'Available'),
            ('Inconsistent','Inconsistent'),
            ('Failed','Failed')
        ],
        verbose_name='SSL Status',
        null=False,
        blank=True,
        max_length=13
    )
    created_at = models.DateTimeField(
        verbose_name="Registration date",
        auto_now_add=True,
        null=False,
        blank=False
    )
    product_name = models.CharField(
        choices = [
            ('ixc_provedor','ixc_provedor'), 
            ('central_assinante','central_assinante'), 
            ('site','site'), 
            ('ixc_franquia','ixc_franquia'), 
            ('speedtest','speedtest'), 
            ('opa_suite','opa_suite'), 
            ('acs','acs'),
        ],
        verbose_name='Product name',
        null=False,
        blank=True,
        max_length=17
    )