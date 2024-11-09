from django.db import models

# Create your models here.
class Message(models.Model):
    theme = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']

    