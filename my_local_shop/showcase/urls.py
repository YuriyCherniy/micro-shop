from django.urls import path

from .views import (
    ItemCreateView,
    ItemDetailView,
    ItemListView,
    ItemDeleteView,
    ItemUpdateView
)


urlpatterns = [
    path('', ItemListView.as_view(), name='item_list_url'),
    path('add-item', ItemCreateView.as_view(), name='item_create_url'),
    path('item-<int:pk>/', ItemDetailView.as_view(), name='item_detail_url'),
    path('item-<int:pk>/delete', ItemDeleteView.as_view(), name='item_delete_url'),
    path('item-<int:pk>/update', ItemUpdateView.as_view(), name='item_update_url')
]
