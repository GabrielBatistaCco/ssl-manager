from app_ssl.utils.serializers import EmailQueueSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from datetime import datetime, timedelta
from app_ssl.models import EmailQueue

class EmailQueueManager:
    serializer = EmailQueueSerializer()

    def __init__(self, data):
        self.domain = data.get('domain')
        self.to_email = data.get('to_email')
        self.status_ssl = data.get('status_ssl')
        self.expiration_ssl = data.get('expiration_ssl')
        self.product_id = data.get('product_id')
        self.issuer = data.get('issuer')

    @transaction.atomic
    def add_notification_to_queue(self):
        notification_criteria = (
            self.to_email
            and self.status_ssl == 'last_month'
            and self.product_id
            and self.issuer and self.issuer.lower() == "sectigo limited"
        )

        if notification_criteria:
            today = datetime.now().date()
        
            notification_in_queue = EmailQueue.objects.filter(
                added_at__range = [today - timedelta(days=300), today],
                domain = self.domain,
                sent__in = ['success', 'waiting'],
            )

            notifications_failed = EmailQueue.objects.filter(
                added_at__range = [today - timedelta(days=300), today],
                domain = self.domain,
                sent = 'failed',
            ).count()

            if not notification_in_queue and notifications_failed < 3:
                EmailQueue.objects.create(
                    to_email = self.to_email,
                    domain = self.domain,
                    expiration_ssl = self.expiration_ssl,
                    sent_at = None,
                    sent = 'waiting',
                )

            return True
        else:
            return False
    
    def send_notification(data):
        domain = data.domain
        expiration_date = data.expiration_ssl
        expiration_ssl = expiration_date.strftime("%d/%m/%Y %H:%M:%S")

        subject = "IXCSoft - Últimos dias para regularizar seu certificado SSL!"
        body = f"""
            <table border="0" cellpadding="0" cellspacing="0" style="border-spacing: 0; border-collapse: collapse; display: table; margin: 0 auto; width: 760px; background: #ffffff;" width="790px">
	            <thead>
	            </thead>
	            <tbody>
		            <tr style="border-spacing: 0; border-collapse: collapse; width: 790px; overflow: hidden; background: #ffffff;">
			            <td style="float: left; margin-top: 0px; box-sizing: border-box; border-spacing: 0; overflow: hidden;  border-collapse: collapse; padding-bottom: 30px;  padding-top: 0px;" width="790px">&nbsp;
			            <table style="margin: 0 auto 20px;" width="790px">
				            <thead style="width: 790px; float: left; clear: left; display: table; border-spacing: 0; border-collapse: collapse;overflow: hidden;">
				            </thead>
				            <tbody>
					            <tr style="width: 780px; background: #ffffff; display: table; border-spacing: 1px; border-color: #ffffff;">
						            <td style="width: 790px; font-family: 'Montserrat', sans-serif; font-weight: 600; color: #5f6060; font-size: 15px; height: 135px; line-height: 22px; padding: 5px 5px 5px 22px; box-sizing: border-box;  background: #ffffff; "><br />
						            <strong>Prezado(a) cliente.</strong><br />
						            <br />
						            Estamos entrando em contato para informar que a validade do seu certificado SSL está próximo do prazo de validade!<br />
						            <br />
                                    <strong> * Domínio:</strong> {domain}<br />
                                    <strong> * Validade:</strong> {expiration_ssl}<br />
                                    <br />
						            <strong>
                                    Entre em contato com nossa equipe para regularizar o certificado SSL!

                                    A depender do produto que você possuí, o departamento de suporte é diferente, seguindo pelos respectivos:

                                    IXCProvedor, IXCFranquia, SpeedTest: SUP - Instalação e Manutenção de Servidor - IXC Provedor
                                    IXC ACS: ACS - Suporte - IXC ACS
                                    Opa!Suite: OPA - Suporte e manutenção de servidores - Opa! Suite
                                    </strong><br />
					            </tr>
					            <tr style="border-spacing: 0; border-collapse: collapse; width: 790px; overflow: hidden;">
						            <td style="float: left; margin-top: 0px; box-sizing: border-box; width: 790px; border-spacing: 0; overflow: hidden;  border-collapse: collapse;" width="790px">&nbsp;</td>
					            </tr>
				            </tbody>
			            </table>
			            </td>
		            </tr>
	            </tbody>
            </table>
        """

        try:
            teste = send_mail(
                subject = subject,
                message = None,
                html_message = body,
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [data.to_email],
                fail_silently=False,
            )
            print(teste)
            return 'success'
        except Exception as e:
            print(str(e))
            return str(e)
