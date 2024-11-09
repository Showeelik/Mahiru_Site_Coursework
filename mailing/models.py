from django.db import models

# Create your models here.
class Mailing(models.Model):
    status = models.CharField(choices=[
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ])
    message = models.ForeignKey('messages.Message')
    recipients = models.ManyToManyField('accounts.User')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['id']
        
        
class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ])
    mail_server_response = models.TextField()

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['id']
        
    def __str__(self):
        return str(self.id)