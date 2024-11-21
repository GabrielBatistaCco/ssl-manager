from django.core.management import call_command
from datetime import datetime

def refresh_certificates():
    print(f'[{datetime.now()}] TASK: Refreshing certificates...')
    call_command('refresh_certificates')

def send_notifications():
    print(f'[{datetime.now()}] TASK: Sending notifications...')
    call_command('send_notifications')
