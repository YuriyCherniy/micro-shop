from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)

from utils import AddPhoneNumberToContextMixin
from .forms import ItemModelForm
from .models import Item


class ItemList(AddPhoneNumberToContextMixin, ListView):
    model = Item
    paginate_by = 9


class ItemDetail(AddPhoneNumberToContextMixin, DetailView):
    model = Item


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'description', 'image', 'price']
    success_message = 'Товар успешно добавлен'
    raise_exception = True

    def post(self, request):
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()
            messages.success(request, self.success_message)
            return redirect(new_item)
        return render(request, 'showcase/item_form.html', {'form': form})


class ItemUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['title', 'description', 'image', 'price']
    success_message = 'Описание товара успешно отредактировано'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        '''
        Method redifinition for image format validaitig
        and adding a default image to form
        '''

        # add a default image to form if the user has not made a choice
        try:
            request.FILES['image']
        except KeyError:
            request.FILES['image'] = Item.objects.get(pk=kwargs['pk']).image

        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            return super().post(request, *args, **kwargs)
        return render(
            request, 'showcase/item_update_form.html', {'form': form}
        )


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        '''
        Django messages framework requires to redefine
        delete method to add flash message
        '''
        messages.success(request, 'Товар успешно удалён')
        return super().delete(request, *args, **kwargs)
