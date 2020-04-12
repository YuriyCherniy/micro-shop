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

from .forms import ItemModelForm
from .models import Item
from mainpage.models import ItemOnMainPage


class ItemList(ListView):
    model = Item
    paginate_by = 9


class ItemsWithoutMainPageItemsList(ListView):
    model = Item
    template_name = 'showcase/item_list.html'

    def get_queryset(self):
        items = ItemOnMainPage.objects.all()
        pk_list = [item.item_on_main_page_id for item in items]
        return Item.objects.exclude(pk__in=pk_list)


class ItemDetail(DetailView):
    model = Item


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'description', 'image', 'price', 'category']
    success_message = 'Товар успешно добавлен'
    raise_exception = True

    def get(self, request):
        count = Item.objects.count()
        if count == 100:
            messages.warning(request, 'Нельзя добавить больше 100 товаров')
            return redirect('/')
        return super().get(request)

    def post(self, request):
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()
            messages.success(request, self.success_message)
            return redirect(new_item)
        return render(request, 'showcase/item_form.html', {'form': form})


class ItemUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = ['title', 'description', 'image', 'price', 'category']
    success_message = 'Описание товара успешно отредактировано'
    template_name = 'showcase/item_update_form.html'
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

        obj = Item.objects.get(pk=kwargs['pk'])
        return render(
            request, 'showcase/item_update_form.html', {'form': form, 'object': obj}
        )


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        '''
        If the item is presented on the main page, reorder
        the position of the dependent items on main page
        and add flash message
        '''

        item = Item.objects.get(pk=kwargs['pk'])
        if hasattr(item, 'itemonmainpage'):
            repositioned_items = ItemOnMainPage.objects.filter(
                position__gt=item.itemonmainpage.position
            )
            for item in repositioned_items:
                item.position -= 1
                item.save()

        messages.success(request, 'Товар успешно удалён')
        return super().delete(request, *args, **kwargs)


class CategoryItemList(ListView):
    '''
    This class shows items by categories
    '''
    model = Item
    paginate_by = 9

    def get_queryset(self):
        return Item.objects.filter(category_id=self.kwargs['pk'])
