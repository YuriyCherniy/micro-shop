from django.forms import ModelForm

from color_theme.models import ColorTheme


class ColorThemeForm(ModelForm):
    class Meta:
        model = ColorTheme
        fields = ['colors']
