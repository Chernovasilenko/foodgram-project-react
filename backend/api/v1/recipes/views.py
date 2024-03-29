from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.v1.permissions import IsAdminOrAuthorOrReadOnly
from api.v1.recipes.filters import IngredientFilter, RecipeFilter
from api.v1.recipes.serializers import (
    TagGetSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateUpdateSerializer,
)
from api.v1.users.serializers import FavoriteSerializer, ShoppingCartSerializer
from api.v1.recipes.utils import RecipeProcessor, get_shopping_cart
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    ShoppingCart,
    FavoriteRecipe
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


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
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
        recipe_processor = RecipeProcessor()
        err_msg = 'Рецепта нет в избранном.'
        return recipe_processor.execute(
            FavoriteSerializer, FavoriteRecipe, request, pk, err_msg
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""
        recipe_processor = RecipeProcessor()
        err_msg = 'Рецепт отсутствует в списке покупок.'
        return recipe_processor.execute(
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
