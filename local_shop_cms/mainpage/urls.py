from django.urls import path

from .views import (
    MainPageEditorList,
    MainPageEditorDelete,
    MainPageEditorCreate,
    MainPageEditorUpdate
)


urlpatterns = [
    path('', MainPageEditorList.as_view(), name='main_page_editor_url'),
    path('<int:pk>/delete', MainPageEditorDelete.as_view(), name='delete_item_from_main_page_url'),
    path('<int:pk>/update', MainPageEditorUpdate.as_view(), name='update_item_on_main_page_url'),
    path('add-item/', MainPageEditorCreate.as_view(), name='add_item_to_main_page_url')
]
