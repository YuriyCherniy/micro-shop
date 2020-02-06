from django.urls import path

from .views import (
    ItemCreate,
    ItemDetail,
    ItemList,
    ItemDelete,
    ItemUpdate
)


urlpatterns = [
    path('', ItemList.as_view(), name='item_list_url'),
    path('create-item/', ItemCreate.as_view(), name='item_create_url'),
    path('item-<int:pk>/', ItemDetail.as_view(), name='item_detail_url'),
    path('item-<int:pk>/delete/', ItemDelete.as_view(), name='item_delete_url'),
    path('item-<int:pk>/update/', ItemUpdate.as_view(), name='item_update_url')
]
