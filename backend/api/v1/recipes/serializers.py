from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.recipes.fields import Base64ImageField
from api.v1.users.serializers import UserGetSerializer
from core import constants as const
from recipes.models import (
    FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)


class TagGetSerializer(serializers.ModelSerializer):
    """Сериализатор получения информации о тегах."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте."""

    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор получения информации о рецептах."""

    tags = TagGetSerializer(
        many=True,
        read_only=True,
    )
    author = UserGetSerializer(
        read_only=True,
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredients',
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        extra_fields = ('is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        """Проверка наличия рецепта в избранном."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and FavoriteRecipe.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверка наличия рецепта в списке покупок."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )


class IngredientPostSerializer(serializers.ModelSerializer):
    """Сериализатор добавления ингредиентов в рецепт."""

    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(
        min_value=const.MIN_VALUE,
        max_value=const.MAX_VALUE,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )

    ingredients = IngredientPostSerializer(
        many=True,
        source='recipe_ingredients',
        required=True
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=const.MIN_VALUE,
        max_value=const.MAX_VALUE
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, ingredients):
        """Проверка поля с ингредиентами."""
        if not ingredients:
            raise ValidationError(
                'В рецепте должны быть ингридиенты!'
            )
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient.get('amount') == 0:
                raise ValidationError(
                    'Количество ингредиента не может быть равным нулю!'
                )
            try:
                ingredient = Ingredient.objects.get(id=ingredient.get('id'))
            except Ingredient.DoesNotExist:
                raise ValidationError('Указан несуществующий ингредиент!')
            if ingredient in ingredients_list:
                # Я не понимаю, это фронт только такого вида ответ может
                # прочитать, или нужно что-то в бэкенде настраивать, но
                # у меня получилось только таким образом сделать так,
                # чтобы сообщение на фронте выводилось
                # Если я правильно понял доку, то этим валидатором так
                # можно пользоваться
                raise ValidationError(
                    [{'ingredients': ['Ингредиенты не могут повторяться!']}]
                )
            ingredients_list.append(ingredient)
        return ingredients

    def validate_tags(self, tags):
        """Проверка поля с тегами."""
        if not tags:
            raise ValidationError(
                'В рецепте должен быть минимум один тег!'
            )
        if len(set(tags)) != len(tags):
            raise ValidationError('Теги не могут повторяться!')
        return tags

    @staticmethod
    def add_ingredients(ingredients, recipe):
        """Добавляет ингредиенты в рецепт."""
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецепта."""
        request = self.context.get('request')
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)
        return recipe
        # return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        """Редактирование рецепта."""
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.add_ingredients(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Добавление информации о рецепте в ответ запроса."""
        return RecipeGetSerializer(instance, context=self.context).data
