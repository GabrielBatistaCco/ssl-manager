from django.contrib import admin
from app_ssl.models import Cert, AuditLog

admin.site.register(Cert)
admin.site.register(AuditLog)
