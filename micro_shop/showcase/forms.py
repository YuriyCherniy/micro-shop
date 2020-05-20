from django.forms import ModelForm, ValidationError
from django.core.files.images import get_image_dimensions

from .models import Item


class ItemModelForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'title', 'description', 'image', 'price', 'category', 'is_archived'
        ]

    def clean_image(self):
        '''
        Only 1×1 format is allowed
        '''
        image = self.cleaned_data.get('image')

        if image.size > 1000000:
            raise ValidationError('Размер изображения не должен превышать 1 мегабайта!')

        width, height = get_image_dimensions(image)
        if width == height:
            return image
        raise ValidationError('Формат изображения должен быть 1×1!')
