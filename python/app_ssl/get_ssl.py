import ssl
import socket
from datetime import datetime
from OpenSSL import crypto

class GetSSLCert:
    def __init__(self, dominio=None, status_ssl=None, validade_ssl=None, timeout=3):
        self.dominio = dominio
        self.status_ssl = status_ssl
        self.timeout = timeout
        self.validade_ssl = validade_ssl

    def get_validade_ssl(self):
        try:
            cert = ssl.get_server_certificate((self.dominio, 443))
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

            get_validade = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            validade_ssl = get_validade.strftime("%Y-%m-%d")
            issuer = x509.get_issuer().O
            
            return {
                'validade_ssl': validade_ssl,
                'issuer': issuer
            }
        except (ssl.SSLError, socket.gaierror, socket.timeout):
            return {
                'validade_ssl': None,
                'issuer': None
            }

    def get_status_ssl(self):

        if self.status_ssl == 'UNUSED':
            return {
                'dominio': None,
                'validade_ssl': None,
                'status_ssl': 'Disponível'
            }

        elif self.validade_ssl is not None:

            validade_ssl = datetime.strptime(
                self.validade_ssl,
                '%Y-%m-%d'
            )

            # print(self.dominio,'--->', validade_ssl, datetime.now())

            if validade_ssl > datetime.now():
                return {
                    'status_ssl': 'Ativo'
                }
            elif validade_ssl == datetime.now():
                return {
                    'status_ssl': 'Último dia'
                }
            else:
                return {
                    'status_ssl': 'Vencido'
                }

        else:
            return {
                'status_ssl': 'Inativo',
            }
