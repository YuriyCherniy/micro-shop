from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from staff.models import UserProfile
from showcase.models import Item


class TestViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.item = Item.objects.create(
            title='some title',
            description='some description',
            image='1.jpg',
            price=100
        )
        self.user = User.objects.create_superuser(
            username='test', email='test@mail.ru', password='0000'
        )
        self.profile = UserProfile.objects.create(
            user_id=1, phone_number='+79615672273'
        )

    def test_item_delete_view_status_code_403(self):
        response = self.c.get(reverse('item_delete_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_item_create_view_status_code_403(self):
        response = self.c.get(reverse('item_create_url'))
        self.assertEquals(response.status_code, 403)

    def test_item_update_view_status_code_403(self):
        response = self.c.get(reverse('item_update_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_item_delete_view_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEquals(response.status_code, 302)
        response = self.c.get(reverse('item_delete_url', args=[1]))

    def test_item_list_view_add_phone_number_to_context_mixin(self):
        response = self.c.get(reverse('item_list_url'))
        self.assertEquals(
            response.context['phone_number'], self.profile.phone_number
        )
