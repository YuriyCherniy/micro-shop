# Generated by Django 2.2.10 on 2020-04-22 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0049_auto_20200422_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='branding',
            new_name='brand',
        ),
    ]