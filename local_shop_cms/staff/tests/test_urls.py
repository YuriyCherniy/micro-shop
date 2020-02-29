from django.test import SimpleTestCase
from django.urls import reverse, resolve

from staff.views import UserProfileUpdate


class TestUrls(SimpleTestCase):

    def test_profile_url_resolved(self):
        url = reverse('profile_url', args=[1])
        self.assertEquals(resolve(url).func.view_class, UserProfileUpdate)
