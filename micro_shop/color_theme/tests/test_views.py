from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from staff.models import UserProfile
from color_theme.models import ColorTheme


class TestView(TestCase):

    def setUp(self):
        self.c = Client()

        User.objects.create_superuser(
            username='test', email='test@test.ru', password='test'
        )
        UserProfile.objects.create(
            user_id=1
        )

    # ststus code 403 test
    def test_color_theme_update_view_status_code_403(self):
        response = self.c.get(reverse('color_theme_update_url'))
        self.assertEqual(response.status_code, 403)

    # status code 302 test
    def test_color_theme_update_view_status_code_302_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.post(reverse('color_theme_update_url'))
        self.assertEqual(response.status_code, 302)

    # template used tests
    def test_color_theme_update_template_used_get(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('color_theme_update_url'))
        self.assertTemplateUsed(response, 'color_theme/color_theme_form.html')

    def test_color_theme_update_template_used_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.post(reverse('color_theme_update_url'), follow=True)
        self.assertTemplateUsed(response, 'color_theme/color_theme_form.html')

    def test_color_theme_update_view_valid_data_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        self.c.post(
            reverse('color_theme_update_url'),
            {'colors': ['#32CD32 #F08080']},
        )
        self.assertEqual(
            ColorTheme.objects.get(pk=1).colors, '#32CD32 #F08080'
        )

    def test_color_theme_update_view_not_valid_data_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        self.c.post(
            reverse('color_theme_update_url'),
            {'colors': ['no data']},
        )
        self.assertNotEqual(ColorTheme.objects.get(pk=1).colors, 'no data')
