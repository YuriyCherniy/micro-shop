from django.db import models
from django.urls import reverse


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'категории'

    title = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Название категории',
        error_messages={
            'unique': 'Категория с таким названием уже существует!'
        }
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail_url', args=[self.pk])
