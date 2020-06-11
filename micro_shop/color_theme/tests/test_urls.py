from django.urls import reverse, resolve
from django.test import SimpleTestCase

from color_theme.views import ColorThemeUpdate


class TestUrls(SimpleTestCase):

    def test_color_theme_update_is_resolved(self):
        url = reverse('color_theme_update_url')
        self.assertEqual(resolve(url).func.view_class, ColorThemeUpdate)
