from django.core.management.base import BaseCommand
from django.db import IntegrityError

from staff.models import UserProfile


class Command(BaseCommand):
    help = 'Used to create superuser profile.'

    def handle(self, *args, **kwargs):
        try:
            UserProfile.objects.create(user_id=1)
            self.stdout.write('Superuser profile created successfully.')
        except IntegrityError:
            self.stderr.write(
                'Superuser profile already exists or superuser is not created!'
            )
