from django.test import SimpleTestCase

from showcase.forms import ItemModelForm


class TestForms(SimpleTestCase):

    def test_item_model_form_no_data(self):
        form = ItemModelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    #def test_item_model_form_valid_data(self):
    #    form = ItemModelForm(
    #        data={
    #            'title': 'Title',
    #            'description': 'x' * 100,
    #            'price': 100,
    #            'image': None
    #        }
    #    )
    #    self.assertTrue(form.is_valid())
    #    print(form.errors.as_text)