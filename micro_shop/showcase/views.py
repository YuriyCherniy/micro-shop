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

    def get_queryset(self):
        return Item.objects.filter(is_archived=False)


class ItemsWithoutMainPageItemsList(ListView):
    '''
    This class shows all items exclude ones presented
    on main page. It needs for 'Ещё товары' button.
    '''
    model = Item
    paginate_by = 9
    template_name = 'showcase/item_list.html'

    def get_queryset(self):
        items_on_main_page = ItemOnMainPage.objects.all()
        pk_list = [item.item_on_main_page_id for item in items_on_main_page]
        return Item.objects.exclude(pk__in=pk_list).filter(is_archived=False)


class ArchivedItemList(LoginRequiredMixin, ListView):
    model = Item
    paginate_by = 9
    raise_exception = True

    def get_queryset(self):
        return Item.objects.filter(is_archived=True)


class ItemDetail(DetailView):
    model = Item


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
        'title', 'description', 'image', 'price', 'category', 'is_archived'
    ]
    raise_exception = True

    def get(self, request):
        if Item.objects.count() == 500:
            messages.warning(request, 'Нельзя добавить больше 500 товаров')
            return redirect('main_page_url')
        return super().get(request)

    def post(self, request):
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()
            messages.success(request, 'Товар успешно добавлен')
            return redirect(new_item)
        return render(request, 'showcase/item_form.html', {'form': form})


class ItemUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = [
        'title', 'description', 'image', 'price', 'category',  'is_archived'
    ]
    success_message = 'Описание товара успешно отредактировано'
    template_name = 'showcase/item_update_form.html'
    raise_exception = True

    def post(self, request, pk):
        item = Item.objects.get(pk=pk)

        # add a default image to form if the user has not made a choice
        try:
            request.FILES['image']
        except KeyError:
            request.FILES['image'] = item.image

        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():

            # prohibit adding items to the archive from the main page
            if all([hasattr(item, 'itemonmainpage'), form.cleaned_data['is_archived']]):
                messages.warning(
                    request, 'Нельзя поместить в архив товар размещённый на главной странице'
                )
            else:
                return super().post(request, pk)

        return render(
            request, 'showcase/item_update_form.html', {'form': form}
        )


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'
    raise_exception = True

    def delete(self, request, pk):
        '''
        If the item is presented on the main page, reorder
        the position of the dependent items on main page
        and add flash message
        '''

        item = Item.objects.get(pk=pk)
        if hasattr(item, 'itemonmainpage'):
            repositioned_items = ItemOnMainPage.objects.filter(
                position__gt=item.itemonmainpage.position
            )
            for item in repositioned_items:
                item.position -= 1
                item.save()

        messages.success(request, 'Товар успешно удалён')
        return super().delete(request, pk)


class CategoryItemList(ListView):
    '''
    This class shows items by categories
    '''
    model = Item
    paginate_by = 9

    def get_queryset(self):
        items = Item.objects.exclude(is_archived=True)
        items = items.filter(category_id=self.kwargs['pk'])
        return items
