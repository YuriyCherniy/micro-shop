from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinLengthValidator

from category_manager.models import Category


class Item(models.Model):
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['-pub_date']

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='Категория товара',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=30,
        verbose_name='название',
        help_text='Длинна названия не должна превышать 30 символов.'
    )

    image = models.ImageField(
        upload_to='item_images',
        verbose_name='изображение',
        help_text='''Формат изображения должен быть 1×1,
        рекомендуемое разрешение 600×600 пикселей.'''
    )

    description = models.TextField(
        validators=[MinLengthValidator(100)],
        max_length=500,
        verbose_name='описание',
        help_text='Длинна описания должна быть от 100 до 500 символов.'
    )

    price = models.IntegerField(verbose_name='цена')

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item_detail_url', args=[self.pk])
