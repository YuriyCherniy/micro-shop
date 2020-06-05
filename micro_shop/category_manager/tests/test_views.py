from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from showcase.models import Item
from staff.models import UserProfile
from category_manager.models import Category
from category_manager.forms import ItemChoiceForm


class TestViews(TestCase):

    def setUp(self):
        self.c = Client()

        User.objects.create_superuser(
            username='test', email='test@test.ru', password='test'
        )
        UserProfile.objects.create(
            user_id=1
        )

        self.category = Category.objects.create(title='test_category')

        Item.objects.create(
            title='test1', description='test1', price=1, category=self.category
        )

    # status code 403 tests

    def test_category_list_view_status_code_403(self):
        response = self.c.get(reverse('category_list_url'))
        self.assertEqual(response.status_code, 403)

    def test_category_create_view_status_code_403_get(self):
        response = self.c.get(reverse('category_create_url'))
        self.assertEqual(response.status_code, 403)

    def test_category_create_view_status_code_403_post(self):
        response = self.c.post(reverse('category_create_url'))
        self.assertEqual(response.status_code, 403)

    def test_category_detail_view_status_code_403(self):
        response = self.c.get(reverse('category_detail_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_add_item_to_category_view_status_code_403_get(self):
        response = self.c.get(reverse('add_item_to_category_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_add_item_to_category_view_status_code_403_post(self):
        response = self.c.post(reverse('add_item_to_category_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_delete_item_from_category_view_status_code_403_get(self):
        response = self.c.get(
            reverse('delete_item_from_category_url', args=[1])
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_item_from_category_view_status_code_403_post(self):
        response = self.c.post(
            reverse('delete_item_from_category_url', args=[1])
        )
        self.assertEqual(response.status_code, 403)

    def test_category_delete_view_status_code_403_get(self):
        response = self.c.get(reverse('category_delete_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_category_delete_view_status_code_403_post(self):
        response = self.c.post(reverse('category_delete_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_category_update_view_status_code_403_get(self):
        response = self.c.get(reverse('category_update_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_category_update_view_status_code_403_post(self):
        response = self.c.post(reverse('category_update_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    # status code 302 tests
    def test_add_item_to_category_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.post(
            reverse('add_item_to_category_url', args=[1]), {'item': 1}
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_item_from_category_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.post(
            reverse('delete_item_from_category_url', args=[1])
        )
        self.assertEqual(response.status_code, 302)

    # template used tests
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
        response = self.c.post(
            reverse('add_item_to_category_url', args=[1]),
            {'item': 1},
            follow=True
        )
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

    def test_category_detail_context_data_item_list(self):
        Item.objects.create(
            title='test2',
            description='test2',
            price=100,
            category=self.category,
            is_archived=True
        )
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_detail_url', args=[1]))
        self.assertEqual(
            len(response.context['item_list']), 1
        )

    def test_category_detail_context_data_form(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        response = self.c.get(reverse('category_detail_url', args=[1]))
        self.assertIs(
            response.context['form'], ItemChoiceForm
        )

    def test_add_item_to_category_works_correctly(self):
        Item.objects.create(
            title='test2', description='test2', price=100,
        )
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        self.c.post(
            reverse('add_item_to_category_url', args=[1]),
            data={'item': 2}
        )
        self.assertEqual(
            len(Item.objects.filter(category_id=1)), 2
        )

    def test_delete_item_from_category_works_correctly_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': 'test'}
        )
        self.c.post(
            reverse('delete_item_from_category_url', args=[1]),
        )
        item = Item.objects.get(pk=1)
        self.assertIsNone(item.category_id)
