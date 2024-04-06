from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Recipe


class RecipeHandler:
    """Добавление и удаление рецепта."""

    @staticmethod
    def add_recipe(serializer_name, request, recipe):
        """Добавить рецепт."""
        serializer = serializer_name(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_recipe(model, request, err_msg, recipe):
        """Удалить рецепт."""
        obj = model.objects.filter(user=request.user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': err_msg}, status=status.HTTP_400_BAD_REQUEST)

    def execute(self, serializer_name, model, request, pk, err_msg=None):
        """Проверить тип и обработать запрос."""
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Recipe.DoesNotExist:
                raise ValidationError(
                    'Рецепт не существует!'
                )
            return self.add_recipe(serializer_name, request, recipe)
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            return self.delete_recipe(model, request, err_msg, recipe)
