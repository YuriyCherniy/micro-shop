from django import template

from staff.models import UserProfile


register = template.Library()


@register.simple_tag
def get_messenger():
    return UserProfile.objects.first().messenger


@register.simple_tag
def get_telegram_user_link():
    return UserProfile.objects.first().telegram_user_link
