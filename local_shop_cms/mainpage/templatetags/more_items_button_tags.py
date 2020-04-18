from django import template

from mainpage.models import ItemOnMainPage
from showcase.models import Item

register = template.Library()


@register.simple_tag
def showe_more_items_button():
    '''
    if overall items count equals items on main
    page count do not show 'ещё товары' button
    '''
    items_on_main_page = ItemOnMainPage.objects.count()
    items = Item.objects.count()
    return items_on_main_page != items
