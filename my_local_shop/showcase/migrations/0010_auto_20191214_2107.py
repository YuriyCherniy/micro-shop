# Generated by Django 3.0 on 2019-12-14 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0009_auto_20191214_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(help_text='- длинна названия не может превышать 20 символов', max_length=20, verbose_name='название объявления'),
        ),
    ]
