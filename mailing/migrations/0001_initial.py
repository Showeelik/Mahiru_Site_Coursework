# Generated by Django 5.1.3 on 2024-11-15 13:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("messages_mailing", "0001_initial"),
        ("recipients", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mailing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_time", models.DateTimeField(verbose_name="Дата и время запуска")),
                ("end_time", models.DateTimeField(verbose_name="Дата и время окончания")),
                (
                    "status",
                    models.CharField(
                        choices=[("CREATED", "Создана"), ("STARTED", "Запущена"), ("FINISHED", "Завершена")],
                        default="CREATED",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="messages_mailing.message",
                        verbose_name="Сообщение",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mailings",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
                (
                    "recipients",
                    models.ManyToManyField(
                        related_name="mailings", to="recipients.recipient", verbose_name="Получатели"
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "ordering": ["id"],
                "permissions": [("view_all_mailings", "Can view all mailings")],
            },
        ),
        migrations.CreateModel(
            name="MailingAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("attempt_time", models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")),
                (
                    "status",
                    models.CharField(
                        choices=[("SUCCESS", "Успешно"), ("FAILURE", "Не успешно")],
                        default="SUCCESS",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                ("response", models.TextField(blank=True, verbose_name="Ответ")),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mailing.mailing", verbose_name="Рассылка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
                "ordering": ["id"],
            },
        ),
    ]
