from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
    Добавления моделей группы Менеджер
    """

    def handle(self, *args, **options):

        # Список групп и их права
        group_name = "Менеджер"
        group_permissions = [
            ""
        ]

        group, _ = Group.objects.get_or_create(name=group_name)
        for permission in group_permissions:
            group.permissions.add(Permission.objects.get(codename=permission))
            
        group.save()

        self.stdout.write(self.style.SUCCESS(f"Группа {group_name} создана"))
