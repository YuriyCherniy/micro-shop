from io import BytesIO

from PIL import Image

from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from showcase.models import Item
from staff.models import UserProfile
from mainpage.models import ItemOnMainPage
from category_manager.models import Category


def create_test_image(width, height, size):
    file = BytesIO()
    image = Image.new('RGBA', size=(width, height), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return InMemoryUploadedFile(
        file=file,
        field_name='image',
        name='test.png',
        content_type='image/png',
        size=size,
        charset='utf-8'
    )


def add_items_to_db_on_main_page(item_amount):
    for i in range(item_amount):
        Item.objects.create(
            title='test', description='test', image='/test.jpg', price=100
        )
        ItemOnMainPage.objects.create(
            item_on_main_page_id=(i + 2), position=(i + 2)
        )


class TestViews(TestCase):

    def setUp(self):
        # TODO буквы в названиях переменных бесплатные
        self.c = Client()

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
        # TODO Где есть setUp созданием должен быть tearDown с удалением

    # status code 403 tests
    def test_item_delete_view_status_code_403_get(self):
        response = self.c.get(reverse('item_delete_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_item_delete_view_status_code_403_delete(self):
        response = self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_item_create_view_status_code_403_get(self):
        response = self.c.get(reverse('item_create_url'))
        self.assertEqual(response.status_code, 403)

    def test_item_create_view_status_code_403_post(self):
        response = self.c.post(reverse('item_create_url'))
        self.assertEqual(response.status_code, 403)

    def test_item_update_view_status_code_403_get(self):
        response = self.c.get(reverse('item_update_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_item_update_view_status_code_403_post(self):
        response = self.c.post(reverse('item_update_url', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_archived_item_list_view_status_code_403(self):
        response = self.c.get(reverse('archived_items_list'))
        self.assertEqual(response.status_code, 403)

    # status code 302 test
    def test_item_delete_view_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_create_view_more_then_500_items_get_status_code_302(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        for i in range(499):
            Item.objects.create(
                title=f'test{i}', description=f'test{i}',
                image=f'/test{i}.jpg', price=100
            )
        response = self.c.get(reverse('item_create_url'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_valid_data_status_code_302_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('item_create_url'),
            data={
                'title': 'test1', 'description': 'test1' * 10, 'price': 100,
                'image': create_test_image(600, 600, 100), 'is_archived': False
            }
        )
        self.assertEqual(response.status_code, 302)

    # others tests
    def test_create_view_invalid_data_status_code_200_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(reverse('item_create_url'), data={})
        self.assertEqual(response.status_code, 200)

    def test_item_reposition_on_main_page_after_deleting(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        add_items_to_db_on_main_page(2)
        self.c.delete(reverse('item_delete_url', args=[1]))
        self.assertEqual(ItemOnMainPage.objects.get(pk=3).position, 2)

    def test_item_list_view_query_set(self):
        Item.objects.create(
            title='test2', description='test2',
            image='/test2.jpg', price=100, is_archived=True
        )
        response = self.c.get(reverse('item_list_url'))
        self.assertEqual(len(response.context_data['item_list']), 1)

    def test_items_without_main_page_items_list_view_query_set(self):
        Item.objects.create(
            title='test2', description='test2', image='/test2.jpg', price=100
        )
        response = self.c.get(reverse('remain_items_url'))
        self.assertEqual(len(response.context_data['item_list']), 1)

    def test_items_without_main_page_items_list_view_query_set_archived(self):
        Item.objects.create(
            title='test2', description='test2', image='/test2.jpg',
            price=100, is_archived=True
        )
        response = self.c.get(reverse('remain_items_url'))
        self.assertEqual(len(response.context_data['item_list']), 0)

    def test_archived_item_list_view_query_set(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        Item.objects.create(
            title='test2', description='test2', image='/test2.jpg',
            price=100, is_archived=True
        )
        response = self.c.get(reverse('archived_items_list'))
        self.assertEqual(len(response.context_data['item_list']), 1)

    def test_category_item_list_query_set(self):
        Category.objects.create(title='category1')
        Item.objects.create(
            title='test2', description='test2', image='/test2.jpg',
            price=100, category_id=1
        )
        response = self.c.get(reverse('category_item_url', args=[1]))
        self.assertEqual(len(response.context_data['item_list']), 1)

    def test_item_update_view_success_update(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('item_update_url', args=[1]),
            data={
                'title': 'test1', 'description': 'test1' * 10, 'price': 100,
                'image': create_test_image(600, 600, 100), 'is_archived': False
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_item_update_view_unsuccess_update_item_is_in_archive(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('item_update_url', args=[1]),
            data={
                'title': 'test1', 'description': 'test1' * 10, 'price': 100,
                'image': create_test_image(600, 600, 100), 'is_archived': True
            }
        )
        self.assertEqual(response.status_code, 200)

    # untested casees
    # def test_item_update_view_unsuccess_update_item_is_on_main_page(self):
    #     pass

    # def test_item_update_view_the user_has_not_chosen_an_image(self):
    #    pass

    # template used tests
    def test_item_list_view_template_used(self):
        response = self.c.get(reverse('item_list_url'))
        self.assertTemplateUsed(response, 'showcase/item_list.html')

    def test_items_without_main_page_items_list_template_used(self):
        response = self.c.get(reverse('remain_items_url'))
        self.assertTemplateUsed(response, 'showcase/item_list.html')

    def test_archived_item_list_template_used(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('archived_items_list'))
        self.assertTemplateUsed(response, 'showcase/item_list.html')

    def test_item_detail_template_used(self):
        response = self.c.get(reverse('item_detail_url', args=[1]))
        self.assertTemplateUsed(response, 'showcase/item_detail.html')

    def test_item_create_template_used_get(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('item_create_url'))
        self.assertTemplateUsed(response, 'showcase/item_form.html')

    def test_item_create_template_used_invalid_data_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(reverse('item_create_url'), data={})
        self.assertTemplateUsed(response, 'showcase/item_form.html')

    def test_item_create_template_used_valid_data_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('item_create_url'),
            data={
                'title': 'test1', 'description': 'test1' * 10, 'price': 100,
                'image': create_test_image(600, 600, 100), 'is_archived': False
            },
            follow=True
        )
        self.assertTemplateUsed(response, 'showcase/item_detail.html')

    def test_item_update_template_used_get(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('item_update_url', args=[1]))
        self.assertTemplateUsed(response, 'showcase/item_update_form.html')

    def test_item_update_template_used_valid_data_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('item_update_url', args=[1]),
            data={
                'title': 'test1', 'description': 'test1' * 10, 'price': 100,
                'image': create_test_image(600, 600, 100), 'is_archived': False
            },
            follow=True
        )
        self.assertTemplateUsed(response, 'showcase/item_detail.html')

    def test_item_update_template_used_invalid_data_post(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.post(
            reverse('item_update_url', args=[1]),
            data={
                'title': 'test1', 'description': 'test1' * 10, 'price': 100,
                'image': create_test_image(600, 601, 100), 'is_archived': False
            },
            follow=True
        )
        self.assertTemplateUsed(response, 'showcase/item_update_form.html')

    def test_item_delete_template_used_get(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.get(reverse('item_delete_url', args=[1]))
        self.assertTemplateUsed(response, 'showcase/item_confirm_delete.html')

    def test_item_delete_template_used_delete(self):
        self.c.post(
            '/admin/login/', {'username': 'test', 'password': '0000'}
        )
        response = self.c.delete(
            reverse('item_delete_url', args=[1]), follow=True
        )
        self.assertTemplateUsed(response, 'mainpage/main_page_item_list.html')

    def test_category_item_list_template_used(self):
        response = self.c.get(reverse('category_item_url', args=[1]))
        self.assertTemplateUsed(response, 'showcase/item_list.html')
