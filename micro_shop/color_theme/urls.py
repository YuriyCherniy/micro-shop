from django.urls import path

from .views import ColorThemeUpdate


urlpatterns = [
    path('', ColorThemeUpdate.as_view(), name='color_theme_update_url')
]