from django import forms

from showcase.models import Item
from mainpage.models import ItemOnMainPage


class ItemOnMainPageCreateForm(forms.Form):
    item_on_main_page = forms.ModelChoiceField(
        queryset=Item.objects.all().exclude(is_archived=True),
        label='Выберите товар'
    )


class ItemOnMainPageUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        '''
        makes the argument 'choices' of the field 'position' dynamically
        changeable depending on the number of products on the main page
        '''
        super().__init__(*args, **kwargs)
        current_items_quantity = ItemOnMainPage.objects.count()
        self.fields['position'].choices = [
            (i, i) for i in range(1, current_items_quantity + 1)
        ]

    position = forms.TypedChoiceField(
        coerce=int,
        label='Позиция на главной'
    )
