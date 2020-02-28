from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from staff.models import UserProfile


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='test', email='test@mail.ru', password='0000'
        )
        self.profile = UserProfile.objects.create(user_id=1)

    def test_userprofile_str_method(self):
        self.assertEquals(
            self.user.userprofile.__str__(),
            f'Пользователь: {self.user.username}'
        )

    def test_userprofile_get_absolute_url_method(self):
        self.assertEquals(
            self.user.userprofile.get_absolute_url(),
            reverse('profile_url', args=[self.user.userprofile.pk])
        )
