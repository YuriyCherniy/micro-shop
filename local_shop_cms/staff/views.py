from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

from staff.models import UserProfile


class UserProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    success_message = 'Данные обновлены'
    raise_exception = True
    fields = [
        'phone_number', 'telegram_user_link', 'messenger',
        'branding', 'instagram', 'vk', 'facebook', 'twitter',
        'telegram', 'whatsapp'
    ]
