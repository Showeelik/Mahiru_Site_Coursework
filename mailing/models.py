from django.db import models



# Create your models here.
class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="Дата и время запуска")
    end_datetime = models.DateTimeField(null=False, blank=True, verbose_name="Дата и время окончания")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    message = models.ForeignKey("messages.Message", on_delete=models.CASCADE, related_name="mailings", verbose_name="Сообщение")
    recipients = models.ManyToManyField("recipients.Subscriber", related_name="mailings", verbose_name="Получатели")
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="mailings", verbose_name="Владелец")

    def __str__(self):
        return f"Mailing {self.id}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['id']


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    attempt_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='success', verbose_name="Статус попытки")
    response = models.TextField(verbose_name="Ответ сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="attempts", verbose_name="Рассылка")

    def __str__(self):
        return f"Attempt {self.id} for Mailing {self.mailing.id}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['id']