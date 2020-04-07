from django import template

from staff.models import UserProfile


register = template.Library()


@register.simple_tag
def get_social_links():
    return UserProfile.objects.first()
