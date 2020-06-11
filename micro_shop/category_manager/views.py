from django.contrib import messages
from django.shortcuts import redirect, render
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

    def post(self, request, pk):
        form = ItemChoiceForm(request.POST)
        if form.is_valid():
            item = Item.objects.filter(pk=form.cleaned_data['item'].pk)
            item.update(category=pk)
            messages.success(request, 'Товар добавлен в категорию')
        else:
            messages.warning(request, 'Что-то пошло не так')

        return redirect(reverse('category_detail_url', args=[pk]))


class DeleteItemFromCategory(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        template = 'category_manager/item_from_category_confirm_delete.html'
        return render(request, template, {'item': item})

    def post(self, request, pk):
        item = Item.objects.filter(pk=pk)
        category_pk = item[0].category.pk
        item.update(category=None)
        messages.success(request, 'Товар удалён из категории')
        return redirect(
            reverse('category_detail_url', args=[category_pk])
        )
