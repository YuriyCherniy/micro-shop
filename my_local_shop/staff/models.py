from django.db import models
from django.urls import reverse
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
        blank=True,
        verbose_name='номер телефона',
        help_text='Без номера телефона кнопки "Позвонить" и "WhatsApp" не активны.'
    )
    youla = models.URLField(
        blank=True,
        verbose_name='профиль на Юле',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )
    avito = models.URLField(
        blank=True,
        verbose_name='профиль на Avito',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )

    def __str__(self):
        return f'Пользователь: {self.user.username}'

    def get_absolute_url(self):
        return reverse('profile_url', args=[self.pk])
