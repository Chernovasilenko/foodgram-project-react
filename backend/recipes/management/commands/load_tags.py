from django.core.management import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Tag

DATA_TAGS = (
    {'name': 'Завтрак', 'color': '#FF0000', 'slug': 'breakfast'},
    {'name': 'Обед', 'color': '#00FF00', 'slug': 'lunch'},
    {'name': 'Ужин', 'color': '#0000FF', 'slug': 'dinner'}
)


class Command(BaseCommand):
    help = 'Добавление стандартных тегов для рецептов в БД.'

    def handle(self, *args, **kwargs):
        try:
            Tag.objects.bulk_create(Tag(**tag) for tag in DATA_TAGS)
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    'Теги, которые вы пытаетесь загрузить, уже есть в таблице.'
                )
            )
        except Exception as e:
            raise CommandError(
                f'При загрузке тегов произошла ошибка: {e}'
            )
        else:
            self.stdout.write(self.style.SUCCESS('Тэги загружены.'))
