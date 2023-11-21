import ssl, socket
import pandas as pd
from datetime import datetime
from OpenSSL import crypto

class GetSSLCert:
    def __init__(self, dominio, status_ssl=None, validade_ssl=None, issuer=None, url_ssls=None):
        self.dominio = dominio if pd.notna(dominio) else None
        self.validade_ssl = validade_ssl if pd.notna(validade_ssl) else None
        self.issuer = issuer
        self.status_ssl = status_ssl
        self.url_ssls = url_ssls
        self.timeout = 5

    def get_validade_ssl(self):

        if self.dominio is None:
            self.validade_ssl = None
            return {
                'validade_ssl': None,
                'issuer': None
            }

        try:
            with socket.create_connection((self.dominio, 443), timeout=self.timeout) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=self.dominio) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)

            get_validade = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            self.validade_ssl = get_validade.strftime("%Y-%m-%d")
            self.issuer = x509.get_issuer().O

            return {
                'validade_ssl': self.validade_ssl,
                'issuer': self.issuer
            }
        except (OSError, ssl.SSLError, socket.gaierror, socket.timeout):
            self.validade_ssl = None
            return {
                'validade_ssl': None,
                'issuer': None
            }

    def get_status_ssl(self):

        if self.status_ssl == 'UNUSED':
            self.status_ssl = 'Disponível'
        elif self.validade_ssl is not None:
            self.validade_ssl = datetime.strptime(
                self.validade_ssl,
                '%Y-%m-%d'
            )
            now = datetime.now()
            if self.validade_ssl > now:
                self.status_ssl = 'Ativo'
            elif self.validade_ssl == now:
                self.status_ssl = 'Último dia'
            else:
                self.status_ssl = 'Vencido'
        elif self.dominio is not None:
            self.status_ssl = 'Abandonado'
        else:
            self.status_ssl = 'Inativo'
        
        return { 'status_ssl': self.status_ssl }

    def get_certificado(self, validade=True, status=True):
        
        dados_certificado = {
            'dominio' : self.dominio,
            'validade_ssl' : self.validade_ssl,
            'url_ssls': self.url_ssls,
            'issuer' : self.issuer,
            'status_ssl' : self.status_ssl
        }

        if validade:
            dados_certificado.update(self.get_validade_ssl())

        if status:
            dados_certificado.update(self.get_status_ssl())

        # print(dados_certificado)
        return dados_certificado
