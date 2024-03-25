from rest_framework import serializers

from api.v1.users.serializers import UserGetSerializer
from core import constants as const
from recipes.models import (
    FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор краткой информации о рецепте."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
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

    name = serializers.StringRelatedField(
        source='ingredient',
        read_only=True,
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit',
        read_only=True,
    )

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
        """Проверить наличие рецепта в избранном."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and FavoriteRecipe.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверить наличие рецепта в списке покупок."""
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

    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=const.MIN_VALUE,
        max_value=const.MAX_VALUE,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')
