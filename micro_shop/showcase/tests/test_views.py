from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from staff.models import UserProfile
from showcase.models import Item
from mainpage.models import ItemOnMainPage


def add_items_to_db_on_main_page(item_amount):
    for i in range(item_amount):
        Item.objects.create(
            title='test', description='test', image='/test.jpg', price=100
        )
        ItemOnMainPage.objects.create(
            item_on_main_page_id=(i + 2), position=(i + 2)
        )


class TestViews(TestCase):

    def setUp(self):
        self.c = Client()

        User.objects.create_superuser(
            username='test', email='test@mail.ru', password='0000'
        )
        UserProfile.objects.create(
            user_id=1, phone_number='+70000000000'
        )
        Item.objects.create(
            title='test', description='test', image='/test.jpg', price=100
        )
        ItemOnMainPage.objects.create(item_on_main_page_id=1, position=1)

    # status code 403 tests
    def test_item_delete_view_status_code_403_get(self):
        response = self.c.get(reverse('item_delete_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_item_delete_view_status_code_403_delete(self):
        response = self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_item_create_view_status_code_403_get(self):
        response = self.c.get(reverse('item_create_url'))
        self.assertEquals(response.status_code, 403)

    def test_item_create_view_status_code_403_post(self):
        response = self.c.post(reverse('item_create_url'))
        self.assertEquals(response.status_code, 403)

    def test_item_update_view_status_code_403_get(self):
        response = self.c.get(reverse('item_update_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_item_update_view_status_code_403_post(self):
        response = self.c.post(reverse('item_update_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_archived_item_list_view_status_code_403(self):
        response = self.c.get(reverse('archived_items_list'))
        self.assertEqual(response.status_code, 403)




    def test_item_delete_view_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEquals(response.status_code, 302)
        response = self.c.get(reverse('item_delete_url', args=[1]))

    def test_item_reposition_on_main_page_after_deleting(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        add_items_to_db_on_main_page(2)
        self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEquals(ItemOnMainPage.objects.get(pk=3).position, 2)
