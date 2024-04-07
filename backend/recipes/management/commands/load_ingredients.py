import csv
import json

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных для ингридиентов из csv или json.'

    def add_arguments(self, parser):
        parser.add_argument(
            'data_path',
            nargs='?',
            type=str,
            help='Путь к файлу с данными. '
                 'Путь по умолчанию - "data/ingredients.csv"'
        )

    def handle(self, *args, **options):
        data_path = options.get('data_path')
        if data_path:
            file_format = data_path.split('.')[-1]
            if file_format not in ('csv', 'json'):
                raise CommandError(
                    'Данные должны быть в формате csv или json.'
                )
        else:
            data_path, file_format = 'data/ingredients.csv', 'csv'
        try:
            with open(data_path, 'r', encoding='utf-8') as file:
                if file_format == 'csv':
                    data_ingredients = csv.DictReader(
                        file,
                        ('name', 'measurement_unit')
                    )
                if file_format == 'json':
                    data_ingredients = json.load(file)
                Ingredient.objects.bulk_create(
                    Ingredient(
                        name=ingredients.get('name'),
                        measurement_unit=ingredients.get('measurement_unit')
                    ) for ingredients in data_ingredients
                )
        except FileNotFoundError as e:
            raise CommandError(
                f'При загрузке данных произошла ошибка: {e}\n'
                'Проверьте правильность пути к файлу.'
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
