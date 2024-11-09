from django.db import models

# Create your models here.

class Recipient(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    comments = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['id']