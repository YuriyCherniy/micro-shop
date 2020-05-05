from django.urls import path

from .views import (
    CategoryList,
    CategoryCreate,
    CategoryDetail,
    CategoryDelete,
    CategoryUpdate,
    AddItemToCategory,
    DeleteItemFromCategory
)


urlpatterns = [
    path('', CategoryList.as_view(), name='category_list_url'),
    path('create/', CategoryCreate.as_view(), name='category_create_url'),
    path('cat-id-<int:pk>/', CategoryDetail.as_view(), name='category_detail_url'),
    path('cat-id-<int:pk>/delete', CategoryDelete.as_view(), name='category_delete_url'),
    path('cat-id-<int:pk>/update', CategoryUpdate.as_view(), name='category_update_url'),
    path('cat-id-<int:pk>/form', AddItemToCategory.as_view(), name='add_item_to_category_url'),
    path('item-<int:pk>/delete', DeleteItemFromCategory.as_view(), name='delete_item_from_category_url')
]