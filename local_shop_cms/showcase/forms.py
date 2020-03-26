from django.forms import ModelForm, ValidationError
from django.core.files.images import get_image_dimensions

from .models import Item


class ItemModelForm(ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image', 'price', 'category']

    def clean_image(self):
        '''
        Only 1:1 format is allowed
        '''
        image = self.cleaned_data.get('image')
        width, height = get_image_dimensions(image)
        if width == height:
            return image
        raise ValidationError('Формат изображения должен быть 1:1!')
