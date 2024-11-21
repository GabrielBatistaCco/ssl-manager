import ssl
import socket
import re
import pandas as pd
from datetime import datetime, timedelta
from OpenSSL import crypto
from app_ssl.models import Cert
from django.db.models import Q
from django.utils import timezone

class GetSSLCert:    
    def __init__(self, data):
        self.pk = data.get('pk')
        self.domain = data.get('domain')
        self.ssls_url = data.get('ssls_url')
        self.status_ssl = data.get('status_ssl')
        self.activation_ssl = None
        self.expiration_ssl = None
        self.activation_weekday = None
        self.expiration_weekday = None
        self.issuer = None
        self.product_id = self.ssls_url.split(r'user/bundles/view/')[-1] if self.ssls_url else None
        self.x509_domain = None

    def get_certificate(self, dates=True, status=True):
        certificate_data = {
            'domain': self.domain,
            'ssls_url': self.ssls_url,
            'activation_ssl': self.activation_ssl,
            'expiration_ssl': self.expiration_ssl,
            'activation_weekday': self.activation_weekday,
            'expiration_weekday': self.expiration_weekday,
            'issuer': self.issuer,
            'status_ssl': self.status_ssl,
            'product_id': self.product_id,
        }

        if dates:
            certificate_data.update(self.get_certificate_dates())

        if status:
            certificate_data.update(self.get_ssl_status())

        # print(certificate_data)
        return certificate_data

    def get_certificate_dates(self, timeout=5):
        if self.domain is None:
            return {
                'activation_ssl': None,
                'expiration_ssl': None,
                'activation_weekday': None,
                'expiration_weekday': None,
                'issuer': None
            }
        try:
            with socket.create_connection((self.domain, 443), timeout=timeout) as sock:
                context = ssl.create_default_context()
                context.check_hostname = False  # Desativar a verificação do nome do host
                context.verify_mode = ssl.CERT_NONE  # Não verificar o certificado
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)

            get_activation_ssl = datetime.strptime(x509.get_notBefore().decode('utf-8'), "%Y%m%d%H%M%SZ")
            get_expiration_ssl = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")

            self.activation_ssl = timezone.make_aware(get_activation_ssl, timezone=timezone.utc)
            self.expiration_ssl = timezone.make_aware(get_expiration_ssl, timezone=timezone.utc)

            self.activation_weekday = get_activation_ssl.strftime("%A")
            self.expiration_weekday = get_expiration_ssl.strftime("%A")
            self.issuer = x509.get_issuer().O
            self.x509_domain = x509.get_subject().CN
            self.x509_domain = re.escape(self.x509_domain).replace(r'\*', '.*') if self.x509_domain else None

            return {
                'activation_ssl': self.activation_ssl,
                'expiration_ssl': self.expiration_ssl,
                'activation_weekday': self.activation_weekday,
                'expiration_weekday': self.expiration_weekday,
                'issuer': self.issuer
            }
        except (OSError, ssl.SSLError, socket.gaierror, socket.timeout) as e:
            return {
                'activation_ssl': None,
                'expiration_ssl': None,
                'activation_weekday': None,
                'expiration_weekday': None,
                'issuer': None
            }

    def get_ssl_status(self):
        available = self.domain is None and self.ssls_url is not None
        inconsistent = (
            ((self.ssls_url is not None and self.ssls_url.strip() != '') and (self.issuer and self.issuer.lower() != "sectigo limited"))
            or
            (True if self.x509_domain and not re.fullmatch(self.x509_domain, self.domain) else False)
        )

        try:
            # Verifica certificado duplicado (importacao de csv e atualização de status)
            existing_cert = Cert.objects.filter(
                Q(domain=self.domain) | Q(ssls_url=self.ssls_url),
                domain__isnull=False,
                ssls_url__isnull=False,
            ).exclude(pk=self.pk if self is not None else None)

            if existing_cert:
                self.status_ssl = 'duplicated'
                existing_cert.update(status_ssl='duplicated')
            elif available:
                self.status_ssl = 'available'
            elif inconsistent:
                self.status_ssl = 'inconsistent'
            elif self.ssls_url and not self.expiration_ssl:
                self.status_ssl = 'abandoned'
            elif self.expiration_ssl:
                self.activation_ssl = self.activation_ssl.date()
                self.expiration_ssl = self.expiration_ssl.date()
                
                today = datetime.now().date()
                seven_days_later = today + timedelta(days=7)
                thirty_days_later = today + timedelta(days=30)
                abandoned = today - timedelta(days=30)

                if self.expiration_ssl < abandoned:
                    self.status_ssl = 'abandoned'
                elif self.expiration_ssl < today:
                    self.status_ssl = 'expired'
                elif self.expiration_ssl == today:
                    self.status_ssl = 'last_day'
                elif self.expiration_ssl <= seven_days_later:
                    self.status_ssl = 'last_week'
                elif self.expiration_ssl <= thirty_days_later:
                    self.status_ssl = 'last_month'
                else:
                    self.status_ssl = 'active'
            else:
                self.status_ssl = 'no_access'
        except Exception as e:
            print(f'Status: {e}')

        return {'status_ssl': self.status_ssl}