from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from staff.models import UserProfile
from mainpage.models import ItemOnMainPage
from showcase.models import Item


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def setUp(self):
        self.c = Client()

# status code 403 tests
    def test_main_page_editor_list_view_status_code_403(self):
        response = self.c.get(reverse('main_page_editor_url'))
        self.assertEquals(response.status_code, 403)

    def test_main_page_editor_create_view_status_code_403(self):
        response = self.c.get(reverse('add_item_to_main_page_url'))
        self.assertEquals(response.status_code, 403)

    def test_main_page_editor_update_view_status_code_403(self):
        response = self.c.get(
            reverse('update_item_on_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 403)

    def test_main_page_editor_delete_view_status_code_403(self):
        response = self.c.delete(
            reverse('delete_item_from_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 403)

# status code 200 tests
    def test_main_page_item_list_view_status_code_200(self):
        response = self.c.get(reverse('main_page_url'))
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_list_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('main_page_editor_url'))
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_create_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('add_item_to_main_page_url'))
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_update_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(
            reverse('update_item_on_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_delete_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(
            reverse('delete_item_from_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 302)