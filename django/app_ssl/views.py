from .models import Cert
from .get_ssl import GetSSLCert
from .serializers import CertSerializer
from .custom_errors import CustomValidationError
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
import pandas as pd

class CertViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def perform_cert_operation(self, serializer, is_update=False):

        domain_form = serializer.validated_data.get('domain')
        ssls_url_form = serializer.validated_data.get('ssls_url')
        product_name_form = serializer.validated_data.get('product_name')

        get_ssl = GetSSLCert(
            domain=domain_form,
            ssls_url=ssls_url_form
        )

        data_to_validate = {
            "domain": get_ssl.domain,
            "ssls_url": get_ssl.ssls_url,
            "product_name": product_name_form
        }
        serializer.validate_data(data_to_validate)

        try:
            certificate_data = get_ssl.get_certificate(datas=True, status=True)
            serializer.validated_data.update(certificate_data)

            serializer.save()

        except Exception as e:
            return Response({'detail': f'Error obtaining the certificate: {e}'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_cert_operation(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_cert_operation(serializer, is_update=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response({'detail': 'Record deleted successfully.'}, status=status.HTTP_200_OK)
        except Cert.DoesNotExist:
            raise ValidationError({'detail': 'Record not found.'})

class CsvViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def create(self, request, *args, **kwargs):

        if 'file' not in request.FILES:
            return Response({'detail': 'The file was not provided.'}, status=status.HTTP_200_OK)

        csv_file = request.FILES['file']

        try:
            csv_data = pd.read_csv(csv_file)
            filtered_data = self.filter_csv_data(csv_data)

            with ThreadPoolExecutor(max_workers=50) as executor:
                executor.map(self.process_csv_line, filtered_data.itertuples(index=False))

            return Response({'detail': 'Certificates imported successfully.'}, status=status.HTTP_200_OK)

        except pd.errors.EmptyDataError:
            return Response({'detail': 'The CSV file is empty.'}, status=status.HTTP_200_OK)

        except pd.errors.ParserError:
            return Response({'detail': 'The provided file is not a valid CSV file.'}, status=status.HTTP_200_OK)

    @transaction.atomic
    def process_csv_line(self, line):
        csv_domain = line.common_name
        csv_ssls_url = line.details_URL
        csv_status_ssl = line.status
        csv_cert = None

        get_ssl = GetSSLCert(
            domain=csv_domain,
            ssls_url=csv_ssls_url,
            status_ssl=status
        )

        certificate_data = get_ssl.get_certificate(datas=True, status=True)

        if csv_domain is not None and csv_ssls_url is not None:
            csv_cert, created = Cert.objects.get_or_create(domain=csv_domain, ssls_url=csv_ssls_url)
        elif csv_domain is not None and csv_ssls_url is None:
            csv_cert, created = Cert.objects.get_or_create(domain=csv_domain)
        elif csv_domain is None and csv_ssls_url is not None:
            csv_cert, created = Cert.objects.get_or_create(ssls_url=csv_ssls_url)

        for field, value in certificate_data.items():
            setattr(csv_cert, field, value)

        csv_cert.save()

    def filter_csv_data(self, csv_data):
        return csv_data[
            (csv_data['details_URL'].notna()) &
            (csv_data['status'].isin(['ISSUED', 'PAUSED', 'UNUSED'])) &
            (~csv_data['common_name'].astype(str).str.startswith('*'))
        ]


class RefreshCertsViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def list(self, request, *args, **kwargs):

        certs_to_refresh = Cert.objects.all()
        certs_count = certs_to_refresh.count()

        if certs_count == 0:
            return Response({'detail': 'No certificates to update.'}, status=status.HTTP_200_OK)

        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.refresh_certificate, certs_to_refresh)

        return Response({'detail': f'Certificates updated successfully.'}, status=status.HTTP_200_OK)

    @transaction.atomic
    def refresh_certificate(self, cert):
        try:
            get_ssl = GetSSLCert(
                domain=cert.domain,
                ssls_url=cert.ssls_url
            )

            certificate_data = get_ssl.get_certificate(datas=True, status=True)

            Cert.objects.filter(pk=cert.pk).update(**certificate_data)
            print(f'Certificate {cert.domain} updated successfully.')

        except Exception as e:
            print(f'Error updating certificate {cert.domain}: {e}')
