from io import BytesIO

from PIL import Image

from django.test import SimpleTestCase
from django.core.files.uploadedfile import InMemoryUploadedFile

from showcase.forms import ItemModelForm


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


class TestForms(SimpleTestCase):
    def setUp(self):
        self.data = {
            'title': 'test_title`',
            'description': 'test_description' * 10,
            'price': 500, 'is_archived': False
        }

    def test_item_model_form_no_data(self):
        form = ItemModelForm(data={})
        self.assertEqual(len(form.errors), 4)

    def test_item_model_form_clean_image_valid_data(self):
        file_data = {
            'image': create_test_image(600, 600, 1000000)
        }
        form = ItemModelForm(data=self.data, files=file_data,)
        self.assertTrue(form.is_valid())

    def test_item_model_form_clean_image_format_1x1_invalid_data(self):
        file_data = {
            'image': create_test_image(600, 601, 1000000)
        }
        form = ItemModelForm(data=self.data, files=file_data)
        self.assertFalse(form.is_valid())

    def test_item_model_form_clean_image_size_bigger_then_1000000(self):
        file_data = {
            'image': create_test_image(600, 600, 1000001)
        }
        form = ItemModelForm(data=self.data, files=file_data,)
        form.is_valid()
        self.assertFalse(form.is_valid())
