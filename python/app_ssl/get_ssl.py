import ssl
import socket
from datetime import datetime
from OpenSSL import crypto

class GetSSLCert:
    def __init__(self, dominio, timeout=5):
        self.dominio = dominio
        self.timeout = timeout

    def get_certificado(self):
        try:
            cert = ssl.get_server_certificate((self.dominio, 443))
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

            validade = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            validade_ssl = validade.strftime("%Y-%m-%d")
            organizacao = x509.get_subject().CN

            if validade < datetime.now():
                status_ssl = 'Vencido'
            else:
                status_ssl = 'Ativo'

            return {
                'validade_ssl': validade_ssl,
                'organizacao': organizacao,
                'status_ssl': status_ssl
            }
        except (ssl.SSLError, socket.gaierror, socket.timeout):
            return {
                'validade_ssl': None,
                'organizacao': None,
                'status_ssl': 'Inativo',
            }