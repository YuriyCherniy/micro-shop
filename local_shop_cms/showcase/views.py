from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    View
)

from utils import AddPhoneNumberToContextMixin
from .forms import ItemModelForm
from .models import Item


class ItemListView(AddPhoneNumberToContextMixin, ListView):
    model = Item
    paginate_by = 9


class ItemDetailView(AddPhoneNumberToContextMixin, DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, View):
    raise_exception = True
    success_message = 'Товар успешно добавлен'

    def get(self, request):
        form = ItemModelForm()
        return render(request, 'showcase/item_form.html', {'form': form})

    def post(self, request):
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()
            messages.success(request, self.success_message)
            return redirect(new_item)
        return render(request, 'showcase/item_form.html', {'form': form})


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['title', 'description', 'image', 'price']
    success_message = 'Описание товара успешно отредактировано'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            return super().post(request, *args, **kwargs)
        return render(
            request, 'showcase/item_update_form.html', {'form': form}
        )


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'
    success_message = 'Товар успешно удалён'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        '''
        Django messages framework requires to redefine
        delete method to add flash message
        '''
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)
