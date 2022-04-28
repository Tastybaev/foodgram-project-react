from django.contrib.admin import ModelAdmin, display, register

from .models import *


EMPTY = '< Тут Пусто >'

@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)
    search_fields = ('name', 'slug',)
    ordering = ('color',)
    empty_value_display = EMPTY


@register(Ingredients)
class IngredientsAdmin(ModelAdmin):
    list_display = ('name', 'weight',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('weight',)
    empty_value_display = EMPTY


@register(Recipes)
class RecipesAdmin(ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('added_in_favorites',)
    empty_value_display = EMPTY

    @display(description='Общее число добавлений в избранное')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@register(CountOfIngredients)
class CountOfIngredientsAdmin(ModelAdmin):
    list_display = (
        'id', 'ingredients', 'amount', 'get_weight',
        'get_recipes_count',
    )
    readonly_fields = ('get_weight',)
    list_filter = ('ingredients',)
    ordering = ('ingredients',)
    empty_value_display = EMPTY

    @display(description='Единица измерения')
    def get_weight(self, obj):
        try:
            return obj.ingredients.weight
        except CountOfIngredients.ingredients.RelatedObjectDoesNotExist:
            return EMPTY

    @display(description='Количество ссылок в рецептах')
    def get_recipes_count(self, obj):
        return obj.recipes.count()


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipes',)
    list_filter = ('user', 'recipes',)
    empty_value_display = EMPTY
