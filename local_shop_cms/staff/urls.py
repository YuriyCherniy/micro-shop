from django.urls import path

from .views import UserProfileUpdate


urlpatterns = [
    path('<int:pk>/', UserProfileUpdate.as_view(), name='profile_url')
]
