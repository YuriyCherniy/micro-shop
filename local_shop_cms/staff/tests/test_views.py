from django.test import SimpleTestCase, Client
from django.urls import reverse


class TestViews(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_user_profile_detail_view_status_code_403(self):
        response = self.client.get(reverse('profile_url', args=[1]))
        self.assertEquals(response.status_code, 403)