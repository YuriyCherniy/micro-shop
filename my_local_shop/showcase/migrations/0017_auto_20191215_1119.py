# Generated by Django 3.0 on 2019-12-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0016_auto_20191215_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='изображение'),
        ),
    ]
