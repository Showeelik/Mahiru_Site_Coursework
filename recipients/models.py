from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    full_name = models.CharField(max_length=255, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['id']
        permissions = [
            ('view_all_recipients', 'Can view all recipients'),
        ]
