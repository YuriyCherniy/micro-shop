# Generated by Django 3.0 on 2019-12-14 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0011_auto_20191214_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='media/default.jpg', upload_to='media', verbose_name='изображение'),
        ),
    ]
