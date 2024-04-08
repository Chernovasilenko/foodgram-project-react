from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.permissions import IsAdminOrAuthorOrReadOnly
from api.v1.recipes.filters import IngredientFilter, RecipeFilter
from api.v1.recipes.mixins import CreateListDestroyPatchMixin
from api.v1.recipes.serializers import (
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateUpdateSerializer,
    TagGetSerializer,
)
from api.v1.recipes.utils import add_recipe, delete_recipe, get_shopping_cart
from api.v1.users.serializers import FavoriteSerializer, ShoppingCartSerializer
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagGetSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингридиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(CreateListDestroyPatchMixin):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от запроса."""
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateUpdateSerializer

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Добавление/удаление рецепта в избранное."""
        return add_recipe(
            FavoriteSerializer, request, pk
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Добавление/удаление рецепта в избранное."""
        err_msg = 'Рецепта нет в избранном.'
        return delete_recipe(
            FavoriteRecipe, request, err_msg, get_object_or_404(Recipe, id=pk)
        )

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""
        return add_recipe(
            ShoppingCartSerializer, request, pk
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""
        err_msg = 'Рецепт отсутствует в списке покупок.'
        return delete_recipe(
            ShoppingCart, request, err_msg, get_object_or_404(Recipe, id=pk)
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Выгружает список покупок в файл."""
        user = request.user
        if not user.carts.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = (
            RecipeIngredient.objects.filter(recipe__carts__user=user)
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(ingredient_amount=Sum('amount'))
        )
        return get_shopping_cart(ingredients)
