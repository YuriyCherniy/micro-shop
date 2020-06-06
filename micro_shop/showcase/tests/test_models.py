from django.test import TestCase
from django.urls import reverse

from showcase.models import Item


class TestModels(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            title='some title',
            description='some description',
            image='/test.jpg',
            price=100
        )

    def test_item_str_method(self):
        self.assertEquals(self.item.__str__(), self.item.title)

    def test_item_get_absolute_url_method(self):
        self.assertEquals(
            self.item.get_absolute_url(),
            reverse('item_detail_url', args=[self.item.pk])
        )
