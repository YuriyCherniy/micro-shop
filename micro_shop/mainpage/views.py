from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.db import transaction
from django.views.generic import (
    View,
    ListView,
    DeleteView
)

from .models import ItemOnMainPage
from .forms import (
    ItemOnMainPageCreateForm,
    ItemOnMainPageUpdateForm
)


class MainPageItemList(ListView):
    model = ItemOnMainPage
    template_name = 'mainpage/main_page_item_list.html'


class MainPageEditorList(LoginRequiredMixin, ListView):
    model = ItemOnMainPage
    template_name = 'mainpage/main_page_item_editor_list.html'
    raise_exception = True


class MainPageEditorDelete(LoginRequiredMixin, DeleteView):
    model = ItemOnMainPage
    success_url = reverse_lazy('main_page_editor_url')
    template_name = 'mainpage/item_on_main_page_confirm_delete.html'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        '''
        Change items position after deleting one
        and add flash message
        '''
        # TODO можно использовать self.get_object() чтоб получить удаляемый итем
        repositioned_items = ItemOnMainPage.objects.filter(
            position__gt=ItemOnMainPage.objects.get(pk=kwargs['pk']).position
        )
        for item in repositioned_items:
            item.position -= 1
            item.save()

        # TODO сначала сообщение потом реальное удаление - плохо
        messages.success(request, 'Товар успешно удалён с главной')
        return super().delete(request, *args, **kwargs)


class MainPageEditorCreate(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        if ItemOnMainPage.objects.count() == 9:
            messages.warning(
                request, 'Нельзя добавить на главную больше 9 товаров'
            )
            return redirect('main_page_editor_url')

        form = ItemOnMainPageCreateForm()
        return render(
            request, 'mainpage/item_on_main_page_form.html', {'form': form}
        )

    def post(self, request):
        form = ItemOnMainPageCreateForm(request.POST)
        if form.is_valid():
            try:
                # TODO Транзакция тут не нужна - у тебя всего 1 запрос на апдейт. Подсчет все равно будет выполнен
                #  не во время запроса на создание, а до него
                with transaction.atomic():
                    ItemOnMainPage.objects.create(
                        item_on_main_page=form.cleaned_data['item_on_main_page'],
                        position=ItemOnMainPage.objects.count() + 1
                    )
                messages.success(request, 'Товар успешно добавлен на главную')
            except IntegrityError:
                messages.warning(request, 'Этот товар уже есть на главной')
        else:
            # TODO если форма не валидна ты должен ее вернуть чтоб могли показаться ошибки валидации юзеру
            messages.warning(request, 'Что-то пошло не так!')
        return redirect('main_page_editor_url')


class MainPageEditorUpdate(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, pk):
        current_item = ItemOnMainPage.objects.get(pk=pk)

        form = ItemOnMainPageUpdateForm(
            initial={
                'position': current_item.position
            }
        )
        return render(
            request, 'mainpage/item_on_main_page_form.html', {'form': form}
        )

    def post(self, request, pk):

        # rearrange items on the main page
        form = ItemOnMainPageUpdateForm(request.POST)
        if form.is_valid():
            # TODO Опять фильтры вместо гетов
            ItemOnMainPage.objects.filter(
                position=form.cleaned_data['position']
            ).update(
                position=ItemOnMainPage.objects.get(pk=pk).position
            )
            ItemOnMainPage.objects.filter(pk=pk).update(
                position=form.cleaned_data['position']
            )
            messages.success(request, 'Позиция товара успешно изменена')
        else:
            # TODO если форма не валидна ты должен ее вернуть чтоб могли показаться ошибки валидации юзеру
            messages.warning(request, 'Что-то пошло не так!')
        return redirect('main_page_editor_url')
