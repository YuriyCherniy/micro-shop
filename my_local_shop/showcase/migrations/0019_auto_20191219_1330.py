# Generated by Django 2.2.9 on 2019-12-19 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0018_item_pub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-pub_date'], 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
    ]
