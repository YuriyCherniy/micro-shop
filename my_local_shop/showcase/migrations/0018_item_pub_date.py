# Generated by Django 2.2.9 on 2019-12-19 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0017_auto_20191215_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
