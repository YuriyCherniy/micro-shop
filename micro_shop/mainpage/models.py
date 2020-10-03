from django.db import models
from django.shortcuts import reverse

from showcase.models import Item


# TODO как будто это должно быть свойство итема, а не отдельная модель.
class ItemOnMainPage(models.Model):
    class Meta:
        verbose_name = 'товар на главной'
        verbose_name_plural = 'товары на главной'
        ordering = ['position']

    item_on_main_page = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        verbose_name='Товар на главной'
    )
    # TODO позиция явно должна быть уникальной
    position = models.IntegerField()

    def __str__(self):
        # TODO Не хватает позиции для полного счастья
        return self.item_on_main_page.title

    def get_absolute_url(self):
        return reverse('item_detail_url', args=[self.item_on_main_page.pk])
