from django.urls import path

from .views import UserProfileUpdatelView


urlpatterns = [
    path('<int:pk>', UserProfileUpdatelView.as_view(), name='profile_url')
]
