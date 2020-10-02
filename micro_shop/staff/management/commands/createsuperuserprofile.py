from django.core.management.base import BaseCommand
from django.db import IntegrityError

from staff.models import UserProfile


# TODO  переименуй команду, писать без разделителей - не оч
class Command(BaseCommand):
    help = 'Used to create superuser profile.'

    def handle(self, *args, **kwargs):
        try:
            # TODO в целом странная команда. Как будто это стоит делать 1 раз и лучше это сделать через админку
            UserProfile.objects.create(user_id=1)
            self.stdout.write('Superuser profile created successfully.')
        except IntegrityError:
            self.stderr.write(
                'Superuser profile already exists or superuser is not created!'
            )
