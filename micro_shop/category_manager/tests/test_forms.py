from django.test import TestCase

from category_manager.forms import ItemChoiceForm
from showcase.models import Item


class TestForms(TestCase):

    def setUp(self):
        Item.objects.create(
            title='test1', description='test1', price=100
        )
        Item.objects.create(
            title='test2', description='test2', price=100, is_archived=True
        )

    def test_item_choice_form_no_data(self):
        form = ItemChoiceForm(data={})
        self.assertFalse(form.is_valid())

    def test_item_choice_form_valid_data(self):
        item = Item.objects.last()
        form = ItemChoiceForm(data={'item': item.pk})
        self.assertTrue(form.is_valid())

    def test_item_choice_form_is_archived_filtered(self):
        self.assertEqual(
            len(ItemChoiceForm().declared_fields['item'].queryset), 1
        )
