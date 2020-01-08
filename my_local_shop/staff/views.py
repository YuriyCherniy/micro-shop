from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'staff/profile.html'
    raise_exception = True
