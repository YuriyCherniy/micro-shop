from django.test import SimpleTestCase
from django.urls import reverse, resolve

from mainpage.views import (
    MainPageEditorList,
    MainPageEditorCreate,
    MainPageEditorDelete,
    MainPageEditorUpdate
)


class TestUrls(SimpleTestCase):
    def test_main_page_editor_url_resolved(self):
        url = reverse('main_page_editor_url')
        self.assertEquals(resolve(url).func.view_class, MainPageEditorList)

    def test_add_item_to_main_page_url_resolved(self):
        url = reverse('add_item_to_main_page_url')
        self.assertEquals(resolve(url).func.view_class, MainPageEditorCreate)

    def test_delete_item_from_main_page_url_resolved(self):
        url = reverse('delete_item_from_main_page_url', args=[1])
        self.assertEquals(resolve(url).func.view_class, MainPageEditorDelete)

    def test_update_item_on_main_page_url_resolved(self):
        url = reverse('update_item_on_main_page_url', args=[1])
        self.assertEquals(resolve(url).func.view_class, MainPageEditorUpdate)
