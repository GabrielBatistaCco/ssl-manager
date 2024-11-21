from concurrent.futures import ThreadPoolExecutor
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .get_ssl import GetSSLCert
from app_ssl.models import Cert, AuditLog
from app_ssl.utils.serializers import AuditLogSerializer
from app_ssl.utils.notifications import EmailQueueManager

class RefreshCertificates:
    @staticmethod
    def refresh_certificate(cert_data):
        try:
            cert_pk = cert_data['id']
            domain = cert_data['domain']
            ssls_url = cert_data['ssls_url']
            email = cert_data['email']

            get_ssl = GetSSLCert({
                "pk": cert_pk,
                "domain": domain,
                "ssls_url": ssls_url,
            })

            certificate_data = get_ssl.get_certificate()

            email_to_queue = EmailQueueManager({
                "to_email": email,
                "domain": domain,
                "status_ssl": certificate_data['status_ssl'],
                "expiration_ssl": certificate_data['expiration_ssl'],
                "product_id": certificate_data['product_id'],
                "issuer": certificate_data['issuer'],
            })

            email_to_queue.add_notification_to_queue()

            with transaction.atomic():
                cert_instance = Cert.objects.get(pk=cert_pk)

                for key, value in certificate_data.items():
                    setattr(cert_instance, key, value)
                
                cert_instance.user = 'Sys'
                cert_instance.save()

        except Exception as e:
            # return 0
            print(f'RefreshCertificates error [{domain}]: {e}')

    @staticmethod
    def refresh_certificates(certs_to_refresh):
        try:
            certs_count = len(certs_to_refresh)

            if certs_count == 0:
                return Response({'detail': 'no_certificates'}, status=status.HTTP_200_OK)

            with ThreadPoolExecutor() as executor:
                executor.map(RefreshCertificates.refresh_certificate, certs_to_refresh)

            return Response({'detail': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'error'}, status=status.HTTP_200_OK)
