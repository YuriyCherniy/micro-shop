from django.test import TestCase, Client
from django.contrib.auth.models import User

from staff.models import UserProfile


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='test', email='test@mail.ru', password='0000'
        )
        self.profile = UserProfile.objects.create(user_id=1)

    def test_userprofile_str_method(self):
        self.assertEquals(
            self.user.userprofile.__str__(),
            f'Пользователь: {self.user.username}'
        )
