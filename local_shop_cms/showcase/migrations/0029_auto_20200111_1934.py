# Generated by Django 2.2.9 on 2020-01-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0028_auto_20200111_1928'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-sort_position', '-pub_date'], 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterField(
            model_name='item',
            name='sort_position',
            field=models.IntegerField(default=10, verbose_name='Позиция в списке'),
        ),
    ]
