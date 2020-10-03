from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
    View
)

from .models import Category
from showcase.models import Item
from .forms import ItemChoiceForm


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    raise_exception = True


class CategoryCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    fields = ['title']
    success_message = 'Категория успешно добавлена'
    raise_exception = True


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list_url')
    raise_exception = True

    def delete(self, request, **kwargs):
        # TODO Сообщение будет выведено даже если категория удалена. Лучше такое пихать в get_success_url
        #  Так же можно было использовать SuccessMessageMixin
        messages.success(request, 'Категория удалена')
        return super().delete(request, **kwargs)


class CategoryUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    fields = ['title']
    success_url = reverse_lazy('category_list_url')
    success_message = 'Категория переименована'
    raise_exception = True


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['item_list'] = Item.objects.filter(
            category_id=self.kwargs['pk']
        ).exclude(is_archived=True)

        context['form'] = ItemChoiceForm
        return context


class AddItemToCategory(LoginRequiredMixin, View):
    raise_exception = True
    # TODO Используй FormView

    def post(self, request, pk):
        form = ItemChoiceForm(request.POST)
        if form.is_valid():
            # TODO Тебе надо получить 1 объект. Используй .get(), а лучше get_object_or_404()
            item = Item.objects.filter(pk=form.cleaned_data['item'].pk)
            item.update(category=pk)
            # TODO и когда объект 1 менять его через .save()
            messages.success(request, 'Товар добавлен в категорию')
        else:
            messages.warning(request, 'Что-то пошло не так')

        return redirect(reverse('category_detail_url', args=[pk]))


class DeleteItemFromCategory(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, pk):
        # TODO будет 500 если указать не тот айди
        item = Item.objects.get(pk=pk)
        template = 'category_manager/item_from_category_confirm_delete.html'
        return render(request, template, {'item': item})

    def post(self, request, pk):
        item = Item.objects.filter(pk=pk)
        # TODO Почему там .get, а тут .filter()[0]? Гет явно лучше.
        category_pk = item[0].category.pk
        item.update(category=None)
        messages.success(request, 'Товар удалён из категории')
        return redirect(
            reverse('category_detail_url', args=[category_pk])
        )

    # TODO Это должно быть написано так (не считая того что стоило использовать DeleteView )
    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        category_id = item.category_id

        if category_id is None:
            messages.warning(request, 'Товар не состоит ни в одной категории')
            return redirect(reverse('item_detail_url', kwargs={'pk': item.id}))

        item.category = None
        item.save(update_fields=('category',))
        messages.success(request, 'Товар удалён из категории')
        return redirect(reverse('category_detail_url', kwargs={'pk': category_id}))

