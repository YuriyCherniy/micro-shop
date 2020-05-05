from django.db import models
from django.shortcuts import reverse

from showcase.models import Item


class ItemOnMainPage(models.Model):
    class Meta:
        verbose_name = 'товар на главной'
        verbose_name_plural = 'товары на главной'
        ordering = ['position']

    item_on_main_page = models.OneToOneField(
        Item, on_delete=models.CASCADE,
        verbose_name='Товар на главной'
    )
    position = models.IntegerField()

    def __str__(self):
        return self.item_on_main_page.title

    def get_absolute_url(self):
        return reverse('item_detail_url', args=[self.item_on_main_page.pk])
