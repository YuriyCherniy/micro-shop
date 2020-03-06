from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from staff.models import UserProfile
from mainpage.models import ItemOnMainPage
from showcase.models import Item


def add_items_to_db(item_amount):
    for i in range(item_amount):
        Item.objects.create(
            title='test', description='test', image='/test.jpg', price=100
        )
        ItemOnMainPage.objects.create(
            item_on_main_page_id=(i + 2), position=(i + 2)
        )


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='test', email='test@mail.ru', password='0000'
        )
        UserProfile.objects.create(
            user_id=1, phone_number='+70000000000'
        )
        Item.objects.create(
            title='test', description='test', image='/test.jpg', price=100
        )
        ItemOnMainPage.objects.create(item_on_main_page_id=1, position=1)

    def setUp(self):
        self.c = Client()

# status code 403 tests
    def test_main_page_editor_list_view_status_code_403(self):
        response = self.c.get(reverse('main_page_editor_url'))
        self.assertEquals(response.status_code, 403)

    def test_main_page_editor_create_view_status_code_403(self):
        response = self.c.get(reverse('add_item_to_main_page_url'))
        self.assertEquals(response.status_code, 403)

    def test_main_page_editor_update_view_status_code_403(self):
        response = self.c.get(
            reverse('update_item_on_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 403)

    def test_main_page_editor_delete_view_status_code_403(self):
        response = self.c.delete(
            reverse('delete_item_from_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 403)

# status code 200 and 302 tests
    def test_main_page_item_list_view_status_code_200(self):
        response = self.c.get(reverse('main_page_url'))
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_list_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('main_page_editor_url'))
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_create_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('add_item_to_main_page_url'))
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_create_view_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        add_items_to_db(8)
        response = self.c.get(reverse('add_item_to_main_page_url'))
        self.assertEquals(response.status_code, 302)

    def test_main_page_editor_update_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(
            reverse('update_item_on_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 200)

    def test_main_page_editor_delete_view_status_code_200(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(
            reverse('delete_item_from_main_page_url', args=[1])
        )
        self.assertEquals(response.status_code, 302)

# templateUsed test cases
    def test_main_page_item_list_template_used(self):
        response = self.c.get(reverse('main_page_url'))
        self.assertTemplateUsed(response, 'mainpage/main_page_item_list.html')

    def test_main_page_editor_list_view_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('main_page_editor_url'))
        self.assertTemplateUsed(
            response, 'mainpage/main_page_item_editor_list.html')

    def test_main_page_editor_create_view_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('add_item_to_main_page_url'))
        self.assertTemplateUsed(
            response, 'mainpage/item_on_main_page_form.html')

    def test_main_page_editor_create_view_redirect_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        add_items_to_db(8)
        response = self.c.get(
            reverse('add_item_to_main_page_url'), follow=True)
        self.assertTemplateUsed(
            response, 'mainpage/main_page_item_editor_list.html')

    def test_main_page_editor_update_view_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(
            reverse('update_item_on_main_page_url', args=[1])
        )
        self.assertTemplateUsed(
            response, 'mainpage/item_on_main_page_form.html')

    def test_main_page_editor_delete_view_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(
            reverse('delete_item_from_main_page_url', args=[1]), follow=True
        )
        self.assertTemplateUsed(
            response, 'mainpage/main_page_item_editor_list.html')

# more tests
    def test_item_reposition_after_deleting(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        add_items_to_db(2)
        self.c.delete(reverse('delete_item_from_main_page_url', args=[1]))
        self.assertEquals(ItemOnMainPage.objects.get(pk=3).position, 2)

    def test_main_page_editor_create_view_status_code_200_POST(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('add_item_to_main_page_url'),
            {'position': 1}
        )
        self.assertEquals(response.status_code, 200)
