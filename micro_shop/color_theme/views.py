from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ColorTheme
from .forms import ColorThemeForm


# TODO Опять же FormView
class ColorThemeUpdate(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        form = ColorThemeForm()
        return render(
            request, 'color_theme/color_theme_form.html', {'form': form}
        )

    def post(self, request):
        form = ColorThemeForm(request.POST)
        if not form.is_valid():
            messages.warning(request, 'Что-то пошло не так')
        else:
            # TODO если ты хочешь чтоб была только 1 запись в таблице - констрейнты обязательны
            #  и еще раз, 1 объект через .update менять не стоит
            ColorTheme.objects.filter(pk=1).update(
                colors=form.cleaned_data['colors']
            )
        return redirect('color_theme_update_url')
