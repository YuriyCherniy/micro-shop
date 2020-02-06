from django.views.generic import View
from django.contrib.auth.models import User


class AddPhoneNumberToContextMixin(View):
    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=1)
        data = super().get_context_data(**kwargs)
        data['phone_number'] = user.userprofile.phone_number
        return data
