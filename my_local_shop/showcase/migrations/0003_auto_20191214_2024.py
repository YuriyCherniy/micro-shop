# Generated by Django 3.0 on 2019-12-14 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_auto_20191214_1951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.RenameField(
            model_name='item',
            old_name='описание',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='цена',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='название',
            new_name='title',
        ),
    ]
