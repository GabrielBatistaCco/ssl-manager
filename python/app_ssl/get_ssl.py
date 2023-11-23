import ssl
import socket
import re
import pandas as pd
from datetime import datetime
from OpenSSL import crypto

class GetSSLCert:
    def __init__(self, dominio, status_ssl=None, ativacao_ssl=None, validade_ssl=None, emissor=None, url_ssls=None):
        self.dominio = dominio if pd.notna(dominio) else None
        self.ativacao_ssl = ativacao_ssl if pd.notna(ativacao_ssl) else None
        self.validade_ssl = validade_ssl if pd.notna(validade_ssl) else None
        self.emissor = emissor
        self.status_ssl = status_ssl
        self.url_ssls = url_ssls if not re.compile(r'^\s*$').match(url_ssls) else None
        self.timeout = 2.5

    def get_datas_certificado(self):
        try:
            with socket.create_connection((self.dominio, 443), timeout=self.timeout) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=self.dominio) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)

            get_ativacao_ssl = datetime.strptime(x509.get_notBefore().decode('utf-8'), "%Y%m%d%H%M%SZ")
            self.ativacao_ssl = get_ativacao_ssl.strftime("%Y-%m-%d")

            get_validade_ssl = datetime.strptime(x509.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
            self.validade_ssl = get_validade_ssl.strftime("%Y-%m-%d")

            self.emissor = x509.get_issuer().O

            return {
                'ativacao_ssl': self.ativacao_ssl,
                'validade_ssl': self.validade_ssl,
                'emissor': self.emissor
            }
        except (OSError, ssl.SSLError, socket.gaierror, socket.timeout) as e:
            print(f'Erro ao obter datas do certificado: {e}')
            return {
                'ativacao_ssl': None,
                'validade_ssl': None,
                'emissor': None
            }

    def get_status_ssl(self):
        if self.status_ssl == 'UNUSED':
            self.status_ssl = 'Disponível'
        elif self.url_ssls is not None and self.url_ssls.strip() != '' and (self.emissor and self.emissor.lower() == "let's encrypt"):
            self.status_ssl = 'Inconsistente'
        elif self.validade_ssl is not None:
            self.validade_ssl = datetime.strptime(self.validade_ssl, '%Y-%m-%d')
            now = datetime.now()
            if self.validade_ssl > now:
                self.status_ssl = 'Ativo'
            elif self.validade_ssl == now:
                self.status_ssl = 'Último dia'
            else:
                self.status_ssl = 'Vencido'
        # elif (self.dominio and self.url_ssls and self.validade_ssl) is not None:
        #     self.status_ssl = 'Abandonado'
        else:
            self.status_ssl = 'Inativo'

        return {'status_ssl': self.status_ssl}

    def get_certificado(self, datas=True, status=True):
        dados_certificado = {
            'dominio': self.dominio,
            'ativacao_ssl': self.ativacao_ssl,
            'validade_ssl': self.validade_ssl,
            'url_ssls': self.url_ssls,
            'emissor': self.emissor,
            'status_ssl': self.status_ssl
        }

        if datas:
            dados_certificado.update(self.get_datas_certificado())

        if status:
            dados_certificado.update(self.get_status_ssl())

        return dados_certificado
