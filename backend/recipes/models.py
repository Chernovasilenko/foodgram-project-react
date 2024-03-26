from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core import constants as const
from recipes.validators import color_validator

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=const.MAX_LENGHT_NAME_FIELD,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=const.MAX_LENGHT_COLOR_FIELD,
        unique=True,
        validators=[color_validator]
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=const.MAX_LENGHT_SLUG_FIELD,
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=const.MAX_LENGHT_NAME_FIELD,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=const.MAX_LENGHT_NAME_FIELD
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=const.MAX_LENGHT_NAME_FIELD
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=const.MAX_LENGHT_CHAR_FIELD,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(const.MIN_VALUE, const.MIN_VALUE_MSG),)
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Связующая модель рецепт-ингредиент."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(const.MIN_VALUE, const.MIN_VALUE_MSG),)
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        db_table = 'recipes_recipe_ingredient'
        ordering = ('id',)

    def __str__(self):
        return (
            f'{self.recipe.name}: '
            f'{self.ingredient.name} - '
            f'{self.amount}/'
            f'{self.ingredient.unit}'
        )


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_favorite',
            ),
        )

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='carts',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='carts',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        db_table = 'recipes_shopping_cart'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_cart',
            ),
        )

    def __str__(self):
        return f'{self.user} - {self.recipe}'
