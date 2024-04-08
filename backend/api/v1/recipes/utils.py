from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from recipes.models import Recipe


def add_recipe(serializer_name, request, pk):
    """Добавить рецепт."""
    try:
        recipe = Recipe.objects.get(id=pk)
    except Recipe.DoesNotExist:
        raise ValidationError(
            'Рецепт не существует!'
        )
    serializer = serializer_name(
        data={'user': request.user.id, 'recipe': recipe.id},
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_recipe(model, request, err_msg, recipe):
    """Удалить рецепт."""
    obj = model.objects.filter(user=request.user, recipe=recipe)
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': err_msg}, status=status.HTTP_400_BAD_REQUEST)


def get_shopping_cart(ingredients):
    """Получить файл со списком покупок."""
    ingredient_count = {}
    for ingredient in ingredients:
        key = (
            f'{ingredient.get("ingredient__name")} '
            f'({ingredient.get("ingredient__measurement_unit")})'
        )
        ingredient_count[key] = (
            ingredient_count.get(key, 0)
            + ingredient.get('ingredient_amount')
        )
    pdfmetrics.registerFont(
        TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf', 'UTF-8')
    )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; '
        'filename="shopping_list.pdf"'
    )
    page = canvas.Canvas(response)
    page.setFont('DejaVuSans', size=24)
    page.drawString(200, 800, 'Список ингредиентов')
    page.setFont('DejaVuSans', size=16)
    height = 750
    for ingredient, amount in ingredient_count.items():
        page.drawString(75, height, (f'{ingredient} - {amount}'))
        height -= 25
        if height == 25:
            page.showPage()
            height = 775
            page.setFont('DejaVuSans', size=16)
    page.save()
    return response
