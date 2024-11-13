from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mailing.models import Mailing, MailingAttempt
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Отправить рассылку'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
            message = mailing.message
            recipients = mailing.recipients.all()

            for recipient in recipients:
                try:
                    send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=mailing.owner.email,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(
                        response='Успешно отправлено',
                        mailing=mailing
                    )
                    self.stdout.write(self.style.SUCCESS(f'Успешно отправлено на {recipient.email}'))
                except Exception as e:
                    MailingAttempt.objects.create(
                        status='FAILURE',
                        response=str(e),
                        mailing=mailing
                    )
                    self.stdout.write(self.style.ERROR(f'Не удалось отправить на {recipient.email}: {e}'))
            
            mailing.status = 'FINISHED'
            mailing.save()
            self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_id} успешно завершена'))
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка {mailing_id} не найдена'))