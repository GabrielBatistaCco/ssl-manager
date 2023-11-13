import ssl
import socket
from datetime import datetime
from OpenSSL import crypto
import asyncio

class GetSSLCert:
    def __init__(self, dominio, timeout=2):
        self.dominio = dominio
        self.timeout = timeout

    async def get_certificado_async(self):
        loop = asyncio.get_event_loop()
        resultado_ssl = await loop.run_in_executor(None, self.get_certificado)
        return resultado_ssl

    def get_certificado(self):
        try:
            cert = ssl.get_server_certificate((self.dominio, 443))
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            
            validade = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            validade_ssl = validade.strftime("%Y-%m-%d")
            issuer = x509.get_issuer().O

            print(issuer)

            if validade < datetime.now():
                status_ssl = 'Vencido'
            else:
                status_ssl = 'Ativo'

            return {
                'validade_ssl': validade_ssl,
                'issuer': issuer,
                'status_ssl': status_ssl
            }
        except (ssl.SSLError, socket.gaierror, socket.timeout):
            return {
                'validade_ssl': None,
                'issuer': None,
                'status_ssl': 'Inativo',
            }
