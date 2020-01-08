from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='пользователь'
    )
    phone_number = PhoneNumberField(
        blank=True, verbose_name='номер телефона'
    )

    def __str__(self):
        return f'Пользователь: {self.user.username}'
