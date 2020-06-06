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
        image = self.cleaned_data.get('image')

        # only 1000000 bytes max size is allowed
        if image.size > 1000000:
            raise ValidationError(
                'Размер изображения не должен превышать 1 мегабайта!'
            )

        # only 1×1 format is allowed
        width, height = get_image_dimensions(image)
        if width != height:
            raise ValidationError('Формат изображения должен быть 1×1!')
        return image
