from io import BytesIO

from PIL import Image

from django.test import SimpleTestCase
from django.core.files.uploadedfile import InMemoryUploadedFile

from showcase.forms import ItemModelForm


def create_test_image(width, height):
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
        size=45,
        charset='utf-8'
    )


class TestForms(SimpleTestCase):
    def setUp(self):
        self.data = {
            'title': 'test_title`',
            'description': 'test_description' * 10,
            'price': 500
        }

    def test_item_model_form_no_data(self):
        form = ItemModelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_item_model_form_clean_image_method_valid_format(self):
        file_data = {
            'image': create_test_image(600, 600)
        }
        form = ItemModelForm(data=self.data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_item_model_form_clean_image_method_invalid_format(self):
        file_data = {
            'image': create_test_image(600, 601)
        }
        form = ItemModelForm(data=self.data, files=file_data)
        self.assertFalse(form.is_valid())
