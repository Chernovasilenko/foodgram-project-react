from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import (
    FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Администрирование тегов."""

    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Администрирование ингридиентов."""

    list_display = ('id', 'name', 'unit')
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Администрирование рецептов."""

    list_display = ('id', 'name', 'author', 'favorites_amount', 'get_img')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    list_display_links = ('name',)
    inlines = (RecipeIngredientInline,)
    readonly_fields = ['favorites_amount']

    @admin.display(description='Добавлено в избранное')
    def favorites_amount(self, obj):
        return obj.favorites.count()

    @admin.display(description='Изображение')
    def get_img(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Администрирование избранных рецептов."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Администрирование спископ покупок."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.site_title = 'Административный сайт Foodgram'
admin.site.site_header = 'Администрирование Foodgram'
admin.site.empty_value_display = 'Не задано'
