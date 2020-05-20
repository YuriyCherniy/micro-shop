from django import forms

from showcase.models import Item


class ItemChoiceForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset=Item.objects.all().exclude(is_archived=True),
        label='Выберите товар для добавления в категорию'
    )
