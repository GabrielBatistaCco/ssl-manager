from django.db import models
from django.http import HttpRequest
from datetime import date

class Cert(models.Model):
    id = models.AutoField(primary_key=True)
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
    product_id = models.CharField(
        verbose_name="SSLS product ID", 
        null=True,
        blank=True,
        max_length=10
    )
    activation_ssl = models.DateTimeField(
        verbose_name="Certificate start date",
        null=True,
        blank=True,
        default=None
    )
    expiration_ssl = models.DateTimeField(
        verbose_name="Certificate end date",
        null=True,
        blank=True,
        default=None
    )
    activation_weekday = models.CharField(
        verbose_name="Activation day", 
        null=True,
        blank=True,
        max_length=50
    )
    expiration_weekday = models.CharField(
        verbose_name="Expiration day", 
        null=True,
        blank=True,
        max_length=50
    )
    issuer = models.CharField(
        verbose_name="Issuer",
        null=True,
        blank=True,
        max_length=50
    )
    status_ssl = models.CharField(
        choices=[
            ('active', 'active'),
            ('expired', 'expired'),
            ('abandoned', 'abandoned'),
            ('last_day', 'last_day'),
            ('last_week', 'last_week'),
            ('last_month', 'last_month'),
            ('available', 'available'),
            ('inconsistent','inconsistent'),
            ('failed','failed'),
            ('duplicated','duplicated'),
            ('no_access', 'no_access'),
        ],
        verbose_name='SSL Status',
        null=True,
        blank=True,
        max_length=13
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
            ('orphan','orphan'),
        ],
        verbose_name='Product name',
        null=True,
        blank=True,
        max_length=17
    )
    notes = models.TextField(
        verbose_name='Notes',
        blank=True,
        null=True
    )
    user = models.CharField(
        verbose_name="User",
        null=False,
        blank=False,
        max_length=100,
        default='Sys'
    )
    email = models.CharField(
        verbose_name='Email',
        null=True,
        blank=True,
        max_length=100
    )

    def save(self, *args, **kwargs):
        action = 'insert' if not self.pk else 'update'
        super().save(*args, **kwargs)
        user = self.user if self.user else 'Sys'

        if self.user != 'Sys':
            cert_data = {
                field.name: self._convert_date(getattr(self, field.name))
                for field in self._meta.fields
                if field.name != 'user'
                if field.name != 'id'
            }

            AuditLog.objects.create(
                action=action,
                model_name='Cert',
                record_id=self.pk,
                user=user,
                cert_data=cert_data,
            )

    def delete(self, *args, **kwargs):
        user = self.user if self.user else 'Sys'

        cert_data = {
            field.name: self._convert_date(getattr(self, field.name))
            for field in self._meta.fields
            if field.name != 'user'
            if field.name != 'id'
        }

        AuditLog.objects.create(
            action='delete',
            model_name='Cert',
            record_id=self.pk,
            user=user,
            cert_data=cert_data,
        )
        super().delete(*args, **kwargs)

    def _convert_date(self, value):
        # Converte objetos date para strings antes da serialização
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value

class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    action_choices = (
        ('Insert', 'Insert'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
    )

    action = models.CharField(max_length=10, choices=action_choices)
    model_name = models.CharField(max_length=100)
    record_id = models.PositiveIntegerField()
    user = models.CharField(max_length=50, null=False, blank=False, default='Sys')
    timestamp = models.DateTimeField(auto_now_add=True)
    cert_data = models.JSONField(blank=True, null=True)

def get_authenticated_user(request):
    """
    Obtém o usuário autenticado a partir do objeto request.
    """
    if isinstance(request, HttpRequest) and request.user.is_authenticated:
        return request.user
    return None

class EmailQueue(models.Model):
    id = models.AutoField(primary_key=True)
    to_email = models.EmailField()
    # subject = models.CharField(max_length=255)
    # body = models.TextField()
    expiration_ssl = models.DateTimeField(null=True, blank=True, default=None)
    domain = models.CharField(null=True, blank=True, max_length=100)
    sent = models.CharField(max_length=10, default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.subject