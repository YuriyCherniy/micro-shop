from django.test import SimpleTestCase
from django.urls import reverse, resolve

from category_manager.views import (
    CategoryList,
    CategoryDetail,
    CategoryCreate,
    CategoryDelete,
    CategoryUpdate,
    AddItemToCategory,
    DeleteItemFromCategory
)


class TestUrls(SimpleTestCase):

    def test_category_list_url_is_resolved(self):
        url = reverse('category_list_url')
        self.assertEqual(resolve(url).func.view_class, CategoryList)

    def test_category_create_url_is_resolved(self):
        url = reverse('category_create_url')
        self.assertEqual(resolve(url).func.view_class, CategoryCreate)

    def test_category_detail_url_is_resolved(self):
        url = reverse('category_detail_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, CategoryDetail)

    def test_category_delete_url_is_resolved(self):
        url = reverse('category_delete_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, CategoryDelete)

    def test_category_update_url_is_resolved(self):
        url = reverse('category_update_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, CategoryUpdate)

    def test_add_item_to_category_url_is_resolved(self):
        url = reverse('add_item_to_category_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, AddItemToCategory)

    def test_delete_item_from_category_url_is_resolved(self):
        url = reverse('delete_item_from_category_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteItemFromCategory)
