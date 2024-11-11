from django.db import models

# Create your models here.
class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема сообщения", null=False, blank=True)
    body = models.TextField(verbose_name="Текст сообщения")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']

    