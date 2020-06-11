from django.test import TestCase
from django.urls import reverse

from category_manager.models import Category


class TestModels(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='Test category')

    def test_category_str_method(self):
        self.assertEqual(self.category.__str__(), 'Test category')

    def test_category_get_absolute_url_method(self):
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse('category_detail_url', args=[self.category.pk])
        )
