from django.core.management.base import BaseCommand
from app_ssl.controller import RefreshCertsViewSet
from datetime import datetime

class Command(BaseCommand):
    help = 'Refresh certificates daily at 5:30 AM'

    def handle(self, *args, **options):
        refresh_view = RefreshCertsViewSet()
        refresh_view.list(None)
        self.stdout.write(self.style.SUCCESS(f'[{datetime.now()}] TASK: Successfully refreshed certificates.'))
