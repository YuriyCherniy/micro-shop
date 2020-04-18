from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

from staff.models import UserProfile
from staff.forms import MessengerForm


class UserProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    success_message = 'Данные обновлены'
    raise_exception = True
    fields = [
        'phone_number', 'telegram_user_link', 'instagram',
        'vk', 'facebook', 'twitter', 'telegram', 'whatsapp'
    ]

    def post(self, request, **kwargs):
        messanger_form = MessengerForm(request.POST)
        if messanger_form.is_valid():
            profile = UserProfile.objects.get(pk=kwargs['pk'])
            profile.messenger = messanger_form.cleaned_data['messenger']
            profile.save()
            return super().post(self, request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messanger_form'] = MessengerForm
        return context
