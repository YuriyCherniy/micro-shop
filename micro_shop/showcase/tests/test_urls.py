from django.test import SimpleTestCase
from django.urls import reverse, resolve

from showcase.views import (
    ItemList,
    ItemsWithoutMainPageItemsList,
    ArchivedItemList,
    CategoryItemList,
    ItemCreate,
    ItemDetail,
    ItemDelete,
    ItemUpdate
)


class TestUrls(SimpleTestCase):

    def test_item_list_url_is_resolved(self):
        url = reverse('item_list_url')
        self.assertEqual(resolve(url).func.view_class, ItemList)

    def test_items_without_main_page_items_list_url_is_resolved(self):
        url = reverse('remain_items_url')
        self.assertEqual(
            resolve(url).func.view_class, ItemsWithoutMainPageItemsList
        )

    def test_archived_item_list_url_is_resolved(self):
        url = reverse('archived_items_list')
        self.assertEqual(resolve(url).func.view_class, ArchivedItemList)

    def test_category_item_list_url_is_resolved(self):
        url = reverse('category_item_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, CategoryItemList)

    def test_item_create_is_resolved(self):
        url = reverse('item_create_url')
        self.assertEqual(resolve(url).func.view_class, ItemCreate)

    def test_item_detail_url_is_resolved(self):
        url = reverse('item_detail_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, ItemDetail)

    def test_item_delete_url_is_resolved(self):
        url = reverse('item_delete_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, ItemDelete)

    def test_item_update_url_is_resolved(self):
        url = reverse('item_update_url', args=[1])
        self.assertEqual(resolve(url).func.view_class, ItemUpdate)
