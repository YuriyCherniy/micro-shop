from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from staff.models import UserProfile
from category_manager.models import Category
from showcase.models import Item


class TestViews(TestCase):

    def setUp(self):
        self.c = Client()

        User.objects.create_superuser(
            username='test', email='test@test.ru', password='test'
        )
        UserProfile.objects.create(
            user_id=1
        )

        Item.objects.create(
            title='test', description='test', price=1
        )

        Category.objects.create(title='test')

    # status code 403 tests
    def test_category_list_view_status_code_403(self):
        response = self.c.get(reverse('category_list_url'))
        self.assertEqual(response.status_code, 403)

    def test_category_create_view_status_code_403(self):
        response = self.c.get(reverse('category_create_url'))
        self.assertEqual(response.status_code, 403)

    def test_category_detail_view_status_code_403(self):
        response = self.c.get(reverse('category_detail_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_add_item_to_category_view_status_code_403(self):
        response = self.c.get(reverse('add_item_to_category_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_delete_item_from_category_view_status_code_403(self):
        response = self.c.get(
            reverse('delete_item_from_category_url', args=[1])
        )
        self.assertEqual(response.status_code, 403)

    def test_category_delete_view_status_code_403(self):
        response = self.c.get(reverse('category_delete_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_category_update_view_status_code_403(self):
        response = self.c.get(reverse('category_update_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    # template used
    def test_category_list_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_list_url'))
        self.assertTemplateUsed(
            response, 'category_manager/category_list.html'
        )

    def test_category_create_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_create_url'))
        self.assertTemplateUsed(
            response, 'category_manager/category_form.html'
        )

    def test_category_detail_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_detail_url', args=[1]))
        self.assertTemplateUsed(
            response, 'category_manager/category_detail.html'
        )

    def test_category_update_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_update_url', args=[1]))
        self.assertTemplateUsed(
            response, 'category_manager/category_form.html'
        )

    def test_category_delete_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_delete_url', args=[1]))
        self.assertTemplateUsed(
            response, 'category_manager/category_confirm_delete.html'
        )

    def test_add_item_to_category_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('add_item_to_category_url', args=[1]))
        self.assertTemplateUsed(
            response, 'category_manager/category_detail.html'
        )

    def test_delete_item_from_category_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(
            reverse('delete_item_from_category_url', args=[1])
        )
        self.assertTemplateUsed(
            response, 'category_manager/item_from_category_confirm_delete.html'
        )