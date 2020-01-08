from django.urls import path

from .views import UserProfileDetailView


urlpatterns = [
    path('<int:pk>', UserProfileDetailView.as_view(), name='profile_url')
]