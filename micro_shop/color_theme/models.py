from django.db import models


class ColorTheme(models.Model):
    colors = models.CharField(
        max_length=15,
        choices=[
            ('#30373e #f5f8e9', 'Classic'),
            ('#32cd66 #32cd66', 'Just Green'),
            ('#4682B4 #00CED1', 'Aqua'),
            ('#BA55D3 #EE82EE', 'Violet'),
            ('#000080 #0000FF', 'Navy Blue'),
            ('#DC143C #FF0000', 'Fire Red'),
            ('#f36767 #F08080', 'Light Pink'),
            ('#fa7218 #f28659', 'Very Orange'),
            ('#F08080 #32CD32', 'Pink-Green'),
            ('#32CD32 #F08080', 'Green-Pink')
        ],
        verbose_name='Выберите цветовую схему сайта'
    )
