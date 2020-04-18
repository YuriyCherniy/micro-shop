from django import forms

from staff.models import UserProfile


class MessengerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_messenger = UserProfile.objects.first().messenger
        self.fields['messenger'].initial = initial_messenger

    messenger = forms.ChoiceField(
        choices=[
            ('whatsapp', 'WhatsApp'),
            ('telegram', 'Telegram'),
            ('viber', 'Viber')
        ],
        label='Мессенджер для связи'
    )
