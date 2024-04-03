from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.v1.permissions import IsAdminOrAuthorOrReadOnly
from api.v1.recipes.filters import IngredientFilter, RecipeFilter
from api.v1.recipes.mixins import CreateListDestroyPatchMixin
from api.v1.recipes.serializers import (
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateUpdateSerializer,
    TagGetSerializer,
)
from api.v1.recipes.utils import get_shopping_cart, RecipeHandler
from api.v1.users.serializers import FavoriteSerializer, ShoppingCartSerializer
from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)


class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagGetSerializer
    pagination_class = None


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
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
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Добавление/удаление рецепта в избранное."""
        err_msg = 'Рецепта нет в избранном.'
        return RecipeHandler().execute(
            FavoriteSerializer, FavoriteRecipe, request, pk, err_msg
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""
        err_msg = 'Рецепт отсутствует в списке покупок.'
        return RecipeHandler().execute(
            ShoppingCartSerializer, ShoppingCart, request, pk, err_msg
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Выгружает список покупок в файл."""
        return get_shopping_cart(request)
