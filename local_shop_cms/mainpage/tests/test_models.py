from django.test import TestCase
from django.urls import reverse

from showcase.models import Item
from mainpage.models import ItemOnMainPage


class TestItemOnMainPageModel(TestCase):

    def setUp(self):
        self.item = Item.objects.create(
            title='test title',
            description='test description',
            price=100,
            image='1.jpg'
        )
        self.on_main_page = ItemOnMainPage.objects.create(
            item_on_main_page_id=1,
            position=1
        )

    def test__str__method(self):
        self.assertEquals(self.on_main_page.__str__(), 'Test title')

    def test_get_absolute_url_method(self):
        self.assertEquals(
            self.on_main_page.get_absolute_url(),
            reverse('item_detail_url', args=[self.on_main_page.pk])
        )
