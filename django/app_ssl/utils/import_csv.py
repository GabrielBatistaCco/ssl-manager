import pandas as pd
from django.db import transaction
from app_ssl.models import Cert
from .get_ssl import GetSSLCert
import re
from concurrent.futures import ThreadPoolExecutor
from rest_framework import status
from rest_framework.response import Response
from .certificate_utils import RefreshCertificates

class GetCSVCerts:
    def import_csv(self, csv_file):
        try:
            csv_data = pd.read_csv(csv_file)
            filtered_data = self.filter_csv_data(csv_data)

            with ThreadPoolExecutor(max_workers=40) as executor:
                executor.map(self.process_csv_line, filtered_data.itertuples(index=False))

            return Response({'detail': 'success'}, status=status.HTTP_200_OK)
        except pd.errors.EmptyDataError:
            return Response({'detail': 'no_certificates'}, status=status.HTTP_200_OK)
        except pd.errors.ParserError:
            return Response({'detail': 'invalid'}, status=status.HTTP_200_OK)

    @classmethod
    @transaction.atomic
    def process_csv_line(cls, line):
        csv_domain = line.common_name if pd.notna(line.common_name) else None 
        csv_ssls_url = line.details_URL if pd.notna(line.details_URL) else None
        product_name = None

        ssls_url_exists = Cert.objects.filter(ssls_url=csv_ssls_url).first()

        if not ssls_url_exists:
            patterns = {
                'ixc_franquia': re.compile(r'(ixcfranquia|franquia)'), # sac
                'ixc_provedor': re.compile(r'^(ix|erp|sistema|agility|isp)'),
                'opa_suite': re.compile(r'^(opa|atendimento|suporte|chat)'),
                'site': re.compile(r'^(site|www)'),
                'central_assinante': re.compile(r'^(central|cliente|portal)'),
                'speedtest': re.compile(r'^(speedtest|test|ookla)'),
                'acs': re.compile(r'^(acs)'),
            }

            if csv_domain:
                for product_match, pattern in patterns.items():
                    if pattern.match(csv_domain):
                        product_name = product_match
                        break

            with transaction.atomic():
                get_ssl = GetSSLCert({
                    "domain": csv_domain,
                    "ssls_url": csv_ssls_url,
                })

                certificate_data = get_ssl.get_certificate()
                Cert.objects.create(**certificate_data, product_name=product_name, user='Csv')

    @classmethod
    def filter_csv_data(cls, csv_data):
        return csv_data[
            (csv_data['details_URL'].notna()) &
            (csv_data['status'].isin(['ISSUED', 'PAUSED', 'UNUSED'])) &
            (~csv_data['common_name'].astype(str).str.startswith('*'))
        ]
