from django import forms

from showcase.models import Item


class ItemChoiceForm(forms.Form):
    item = forms.ModelChoiceField(
        # TODO .all() тут не обязательно
        queryset=Item.objects.all().exclude(is_archived=True),
        label='Выберите товар для добавления в категорию'
    )
