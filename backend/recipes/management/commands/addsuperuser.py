import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError

from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@admin.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')


class Command(BaseCommand):
    help = 'Добавление администратора.'

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser(
                ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
            )
        except IntegrityError as e:
            raise CommandError(
                f'При добавлении администратора произошла ошибка: {e}\n'
                'Администратор с таким именем уже существует.'
            )
        except Exception as e:
            raise CommandError(
                f'При добавлении администратора произошла ошибка: {e}'
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Администратор {ADMIN_USERNAME} добавлен.')
            )
