# Generated by Django 4.2.7 on 2023-11-13 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_ssl', '0002_certificado_status_ssl'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Certificado',
            new_name='Cert',
        ),
    ]