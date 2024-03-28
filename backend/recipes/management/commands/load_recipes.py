from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Добавление стандартных тегов для рецептов в БД'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#FF0000', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#00FF00', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#0000FF', 'slug': 'dinner'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Тэги загружены.'))
