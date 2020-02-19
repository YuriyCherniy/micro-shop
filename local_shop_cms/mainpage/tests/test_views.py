from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from staff.models import UserProfile


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='test', email='test@mail.ru', password='0000'
        )
        UserProfile.objects.create(
            user_id=1, phone_number='+70000000000'
        )

    def setUp(self):
        self.c = Client()

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



    def test_main_page_item_list_view_status_code_200(self):
        response = self.c.get(reverse('main_page_url'))
        self.assertEquals(response.status_code, 200)