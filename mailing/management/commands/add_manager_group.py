from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Добавляет группу "Менеджер" с правами на просмотр всех рассылок, сообщений и получателей.'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджер')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджер" успешно создана'))

        content_types = ContentType.objects.filter(
            model__in=['mailing', 'messages_mailing', 'recipients']
        )

        permissions = Permission.objects.filter(
            content_type__in=content_types,
            codename__in=[
                'view_all_mailings',
                'view_all_messages',
                'view_all_recipients',
            ]
        )

        group.permissions.set(permissions)
        group.save()
        self.stdout.write(self.style.SUCCESS('Успешно добавлены права группы "Менеджер"'))