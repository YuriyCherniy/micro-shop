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
        help_text='''
        Без номера телефона кнопки "Позвонить" и "WhatsApp" не активны.
        '''
    )
    instagram = models.URLField(
        blank=True,
        verbose_name='профиль Instagram',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )
    vk = models.URLField(
        blank=True,
        verbose_name='профиль VK',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )

    facebook = models.URLField(
        blank=True,
        verbose_name='профиль Facebook',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )

    twitter = models.URLField(
        blank=True,
        verbose_name='профиль Twitter',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )

    telegram = models.URLField(
        blank=True,
        verbose_name='профиль Telegram',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )

    whatsapp = models.URLField(
        blank=True,
        verbose_name='профиль WhatsApp',
        help_text='Оставьте поле пустым, чтобы не отображать ссылку в футере.'
    )

    telegram_user_link = models.URLField(
        blank=True,
        verbose_name='Ссылка на Telegram UserName',
        help_text='''
        Заполните поле если используете Telegram
        в качестве мессенджера для связи.
        '''
    )

    messenger = models.CharField(
        max_length=10,
        choices=[
            ('whatsapp', 'WhatsApp'),
            ('telegram', 'Telegram')
        ],
        default='whatsapp',
        verbose_name='Мессенджер для связи',
        help_text='Выберите в какой мессенджер перенаправлять пользователя.'
    )

    branding = models.CharField(
        max_length=25,
        default='Главная',
        verbose_name='Брендирование витрины',
        help_text='''Этот текст будет отображаться вместо
        кнопки "Главная" в навигацилнной панели сайта.'''
    )

    def __str__(self):
        return f'Пользователь: {self.user.username}'

    def get_absolute_url(self):
        return reverse('profile_url', args=[self.pk])
