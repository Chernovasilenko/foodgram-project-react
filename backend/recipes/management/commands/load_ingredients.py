import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных для ингридиентов из CSV-файла для базы данных.'

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
                'Проверьте, что в директории "data" находится файл '
                '"ingredients.csv" и он правильно назван.'
            )
        except IntegrityError:
            raise CommandError(
                'Данные, которые вы пытаетесь загрузить, уже есть в таблице.'
            )
        except Exception as e:
            raise CommandError(
                f'При загрузке данных произошла ошибка: {e}'
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Все данные успешно загружены.'
                )
            )
