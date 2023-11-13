# Generated by Django 4.2.7 on 2023-11-13 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ssl', '0003_rename_certificado_cert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cert',
            name='status_ssl',
            field=models.CharField(choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo'), ('Vencido', 'Vencido')], default=None, max_length=10, verbose_name='Status SSL'),
        ),
    ]