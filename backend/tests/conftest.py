import pytest
from rest_framework.test import APIClient

from recipes.models import (
    FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)
from users.models import Subscribe

pytestmark = pytest.mark.django_db


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        username='Автор',
        email='test_user@ya.ru',
        first_name='Test',
        last_name='Testovoi',
        password='qaZ171786T',
    )


@pytest.fixture
def api_client():
    client = APIClient()
    client.enforce_csrf_checks = True
    return client


@pytest.fixture
def author_client(author, api_client):
    api_client.force_authenticate(author)
    return api_client


@pytest.fixture
def recipe(author, ingredient, tag):
    recipe = Recipe.objects.create(
        author=author,
        name='Название рецепта',
        text='Описание рецепта',
        image='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAA'
              'BieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw'
              '4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==',
        cooking_time=60,
    )
    recipe.tags.add(tag.pk)
    RecipeIngredient.objects.create(
        ingredient=ingredient,
        recipe=recipe,
        amount=1
    )
    return recipe


@pytest.fixture
def another_author_client(django_user_model, api_client):
    another_author = django_user_model.objects.create(
        username='Другой автор',
        email='test_user@mail.ru',
        first_name='Другой',
        last_name='автор',
        password='passworTest0104',
    )
    api_client.force_authenticate(another_author)
    return api_client


@pytest.fixture
def author_sub_client(django_user_model, author, api_client, recipe):
    user_sub = django_user_model.objects.create(
        username='Подписчик',
        email='test_sub@mail.ru',
        first_name='подписчик',
        last_name='автор',
        password='passworTest0104',
    )
    Subscribe.objects.create(
        user=user_sub,
        author=author
    )
    FavoriteRecipe.objects.create(
        user=user_sub,
        recipe=recipe
    )
    ShoppingCart.objects.create(
        user=user_sub,
        recipe=recipe
    )
    api_client.force_authenticate(user_sub)
    return api_client


@pytest.fixture
def tag():
    return Tag.objects.create(
        name='Завтрак',
        color='#FF0000',
        slug='breakfast',
    )


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(
        name='ингридиент',
        measurement_unit='г',
    )


@pytest.fixture
def pk_author(author):
    return author.pk,


@pytest.fixture
def user_detail_url(author):
    return f'/api/users/{author.pk}/'


@pytest.fixture
def user_subscribe_url(author):
    return f'/api/users/{author.pk}/subscribe/'


@pytest.fixture
def recipe_url(recipe):
    return f'/api/recipes/{recipe.pk}/'


@pytest.fixture
def tag_url(tag):
    return f'/api/tags/{tag.pk}/'


@pytest.fixture
def ingredient_url_id(ingredient):
    return f'/api/ingredients/{ingredient.pk}/'


@pytest.fixture
def ingredient_url_name(ingredient):
    return f'/api/ingredients/?name={ingredient.name}'


@pytest.fixture
def add_recipe_to_favorite_url(recipe):
    return f'/api/recipes/{recipe.pk}/favorite/'


@pytest.fixture
def add_recipe_to_shopcart_url(recipe):
    return f'/api/recipes/{recipe.pk}/shopping_cart/'
