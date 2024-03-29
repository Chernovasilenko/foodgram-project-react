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
    help = 'Добавление тестового администратора'

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser(
                ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS('Администратор добавлен.'))
        except IntegrityError as e:
            raise CommandError(
                f'При загрузке данных произошла ошибка: {e}\n'
                'Данные, которые вы пытаетесь загрузить, уже есть в таблице'
            )
