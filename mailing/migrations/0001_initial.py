# Generated by Django 5.1.3 on 2024-11-11 14:46

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
                ("start_datetime", models.DateTimeField(auto_now_add=True, verbose_name="Дата и время запуска")),
                ("end_datetime", models.DateTimeField(blank=True, verbose_name="Дата и время окончания")),
                (
                    "status",
                    models.CharField(
                        choices=[("created", "Создана"), ("started", "Запущена"), ("completed", "Завершена")],
                        default="created",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mailings",
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
                        related_name="mailings", to="recipients.subscriber", verbose_name="Получатели"
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="MailingAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "attempt_datetime",
                    models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата и время попытки"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("success", "Успешно"), ("failed", "Не успешно")],
                        default="success",
                        max_length=10,
                        verbose_name="Статус попытки",
                    ),
                ),
                ("response", models.TextField(verbose_name="Ответ сервера")),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attempts",
                        to="mailing.mailing",
                        verbose_name="Рассылка",
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