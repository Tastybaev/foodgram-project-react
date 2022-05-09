from django.db.models import IntegerField, Value, values_list
from django_filters.rest_framework import (
    AllValuesMultipleFilter,
    BooleanFilter,
    CharFilter,
    FilterSet
)

from users.models import ShoppingList
from .models import Ingredient, Recipe


class IngredientSearchFilter(FilterSet):
    name = CharFilter(method='search_by_name')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def search_by_name(self, queryset, name, value):
        if not value:
            return queryset
        start_with_queryset = (
            queryset.filter(name__istartswith=value).annotate(
                order=Value(0, IntegerField())
            )
        )
        contain_queryset = (
            queryset.filter(name__icontains=value).exclude(
                pk__in=(ingredient.pk for ingredient in start_with_queryset)
            ).annotate(
                order=Value(1, IntegerField())
            )
        )
        return start_with_queryset.union(contain_queryset).order_by('order')


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_list = BooleanFilter(method='get_is_in_shopping_list')
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author',)

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorites = self.request.user.favorites.all()
        return queryset.filter(
            pk__in=favorites.objects.values_list(recipe.pk)
        )

    def get_is_in_shopping_list(self, queryset, name, value):
        if not value:
            return queryset
        try:
            recipes = (
                self.request.user.shopping_list.recipes.all()
            )
        except ShoppingList.DoesNotExist:
            return queryset
        return queryset.filter(
            pk__in=recipes.objects.values_list(pk)
        )


class SearhIndigrient(FilterSet):
    name = CharFilter(method='search_by_name')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def search_by_name(self, name):
        if not name:
            return "Имя не найдено!"
        return name.objects.all()
