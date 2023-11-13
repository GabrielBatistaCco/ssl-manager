# Generated by Django 4.2.7 on 2023-11-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ssl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificado',
            name='status_ssl',
            field=models.CharField(choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo'), ('Vencido', 'Vencido')], default='-', max_length=10, verbose_name='Status SSL'),
        ),
    ]
