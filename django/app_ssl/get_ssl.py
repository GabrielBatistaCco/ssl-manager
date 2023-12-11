import ssl
import socket
import re
import pandas as pd
from datetime import datetime, timedelta
from OpenSSL import crypto

class GetSSLCert:
    def __init__(self, domain=None, status_ssl=None, activation_ssl=None, expiration_ssl=None, issuer=None, ssls_url=None):
        self.domain = domain if pd.notna(domain) else None
        self.activation_ssl = activation_ssl if pd.notna(activation_ssl) else None
        self.expiration_ssl = expiration_ssl if pd.notna(expiration_ssl) else None
        self.activation_weekday = None
        self.expiration_weekday = None
        self.issuer = issuer
        self.status_ssl = status_ssl
        self.ssls_url = ssls_url if pd.notna(ssls_url) else None
        self.timeout = 2.5

    def get_certificate_dates(self):

        if self.domain is None:
            return {
                'activation_ssl': None,
                'expiration_ssl': None,
                'activation_weekday': None,
                'expiration_weekday': None,
                'issuer': None
            }
        try:
            with socket.create_connection((self.domain, 443), timeout=self.timeout) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)

            get_activation_ssl = datetime.strptime(x509.get_notBefore().decode('utf-8'), "%Y%m%d%H%M%SZ")
            get_expiration_ssl = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            
            self.activation_ssl = get_activation_ssl.strftime("%Y-%m-%d")
            self.expiration_ssl = get_expiration_ssl.strftime("%Y-%m-%d")
            self.activation_weekday = get_activation_ssl.strftime("%A")
            self.expiration_weekday = get_activation_ssl.strftime("%A")
            self.issuer = x509.get_issuer().O

            return {
                'activation_ssl': self.activation_ssl,
                'expiration_ssl': self.expiration_ssl,
                'activation_weekday': self.activation_weekday,
                'expiration_weekday': self.expiration_weekday,
                'issuer': self.issuer
            }
        except (OSError, ssl.SSLError, socket.gaierror, socket.timeout) as e:
            # print(f'Error obtaining certificate dates: {e}')
            return {
                'activation_ssl': None,
                'expiration_ssl': None,
                'activation_weekday': None,
                'expiration_weekday': None,
                'issuer': None
            }

    def get_ssl_status(self):

        try:
            if self.status_ssl == 'UNUSED' or (self.domain is None and self.ssls_url is not None):
                self.status_ssl = 'Available'
            elif self.ssls_url is not None and self.ssls_url.strip() != '' and (self.issuer and self.issuer.lower() == "let's encrypt"):
                self.status_ssl = 'Inconsistent'
            elif self.expiration_ssl is not None:
                self.expiration_ssl = datetime.strptime(self.expiration_ssl, '%Y-%m-%d').date()

                today = datetime.now().date()
                seven_days_later = today + timedelta(days=7)
                thirty_days_later = today + timedelta(days=30)

                if self.expiration_ssl < today:
                    self.status_ssl = 'Expired'
                elif self.expiration_ssl == today:
                    self.status_ssl = 'Last day'
                elif self.expiration_ssl <= seven_days_later:
                    self.status_ssl = 'Last week'
                elif self.expiration_ssl <= thirty_days_later:
                    self.status_ssl = 'Last month'
                else:
                    self.status_ssl = 'Active'
            else:
                self.status_ssl = 'Inactive'
        except Exception as e:
            print(e)

        return {'status_ssl': self.status_ssl}

    def get_certificate(self, datas=True, status=True):

        certificate_data = {
            'domain': self.domain,
            'activation_ssl': self.activation_ssl,
            'expiration_ssl': self.expiration_ssl,
            'activation_weekday': self.activation_weekday,
            'expiration_weekday': self.expiration_weekday,
            'ssls_url': self.ssls_url,
            'issuer': self.issuer,
            'status_ssl': self.status_ssl
        }

        if datas:
            certificate_data.update(self.get_certificate_dates())

        if status:
            certificate_data.update(self.get_ssl_status())

        print(certificate_data)
        return certificate_data
