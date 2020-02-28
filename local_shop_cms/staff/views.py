from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

from staff.models import UserProfile


class UserProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    fields = ['phone_number', 'youla', 'avito']
    template_name_suffix = '_update_form'
    success_message = 'Данные обновлены'
    raise_exception = True
