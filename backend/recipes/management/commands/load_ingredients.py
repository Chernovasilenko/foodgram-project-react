import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Ingredient

FLUSHING_MESSAGE = (
    '\nПеред следующей загрузкой данных необходимо очистить базу '
    'данных командой "python manage.py flush"'
)


class Command(BaseCommand):
    help = """Импорт данных для ингридиентов из CSV-файла для базы данных"""

    def handle(self, *args, **options):
        try:
            with open('data/ingredients.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=",")
                ingredients_to_create = []
                for row in reader:
                    name, unit = row
                    if name:
                        ingredient = Ingredient(
                            name=name, measurement_unit=unit
                        )
                        ingredients_to_create.append(ingredient)
                Ingredient.objects.bulk_create(ingredients_to_create)
        except FileNotFoundError as e:
            raise CommandError(
                f'При загрузке данных произошла ошибка: {e}\n'
                f'Проверьте, что в директории "data" находится файл '
                f'"ingredients.csv" и он правильно назван'
                f'{FLUSHING_MESSAGE}'
            )
        except IntegrityError as e:
            raise CommandError(
                f'При загрузке данных произошла ошибка: {e}\n'
                'Данные, которые вы пытаетесь загрузить, уже есть в таблице'
                f'{FLUSHING_MESSAGE}'
            )
        except Exception as e:
            raise CommandError(
                f'При загрузке данных произошла ошибка: {e}{FLUSHING_MESSAGE}'
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Все данные успешно загружены'
                )
            )

