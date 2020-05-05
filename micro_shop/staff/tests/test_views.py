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
        UserProfile.objects.create(user_id=1)

    def setUp(self):
        self.c = Client()

    def test_user_profile_update_view_status_code_403(self):
        response = self.c.get(reverse('profile_url', args=[1]))
        self.assertEquals(response.status_code, 403)

    def test_user_profile_update_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('profile_url', args=[1]))
        self.assertEquals(response.status_code, 200)

    def test_userprofile_form_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('profile_url', args=[1]))
        self.assertTemplateUsed(response, 'staff/userprofile_form.html')
