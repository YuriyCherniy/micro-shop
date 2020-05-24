from django import template

from color_theme.models import ColorTheme


register = template.Library()


@register.simple_tag
def get_style_colors():
    '''get colors from db as string and return as dictionary'''

    colors_data = ColorTheme.objects.first().colors.split()
    colors = {
        'nav': colors_data[0], 'footer': colors_data[1]
    }
    return colors

