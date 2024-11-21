from django.core.management.base import BaseCommand
from app_ssl.models import EmailQueue
from app_ssl.utils.notifications import EmailQueueManager
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send notifications by processing the email queue'

    def handle(self, *args, **options):
        email_in_queue = EmailQueue.objects.filter(sent='waiting').first()

        if email_in_queue:
            send_notification = EmailQueueManager.send_notification(email_in_queue)

            if send_notification == 'success':
                email_in_queue.sent = 'success'
                email_in_queue.sent_at = timezone.now()
                email_in_queue.save()
                self.stdout.write(f'[{email_in_queue.domain}]: Notifications to {email_in_queue.to_email} sent successfully.')
            else:
                email_in_queue.sent = 'failed'
                email_in_queue.sent_at = timezone.now()
                email_in_queue.error_message = send_notification
                email_in_queue.save()
                self.stdout.write(f'[{email_in_queue.domain}]: Notifications to {email_in_queue.to_email} failed.')
