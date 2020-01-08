from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)

from .forms import ItemModelForm
from .utils import AddPhoneNumberToContextMixin
from .models import Item


class ItemListView(AddPhoneNumberToContextMixin, ListView):
    model = Item
    paginate_by = 9


class ItemDetailView(AddPhoneNumberToContextMixin, DetailView):
    model = Item


#class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    model = Item
#    fields = ['title', 'description', 'image', 'price']
#    success_message = 'Товар успешно добавлен'
#    raise_exception = True

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
            messages.success(self.request, self.success_message)
            return redirect(new_item)
        return render(request, 'showcase/item_form.html', {'form': form})


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['title', 'description', 'image', 'price']
    template_name_suffix = '_update_form'
    success_message = 'Описание товара успешно отредактировано'
    raise_exception = True


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
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
