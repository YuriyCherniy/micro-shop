from django import template

from staff.models import UserProfile


register = template.Library()


@register.simple_tag
def get_brand():
    '''
    set brand name instead of 'Главная' in the navbar
    '''
    # TODO Если профилей нет - падает
    return UserProfile.objects.first().brand
