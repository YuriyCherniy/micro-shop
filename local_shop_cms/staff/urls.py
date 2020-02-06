from django.urls import path

from .views import UserProfileUpdatel


urlpatterns = [
    path('<int:pk>', UserProfileUpdatel.as_view(), name='profile_url')
]
