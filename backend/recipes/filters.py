from users.models import *
from django_filters.rest_framework import *

from users.models import Shopping_list
from .models import Ingredients, Recipes

ERROR_NAME= "Имя не найдено!"


class IngredientsSearchFilter(FilterSet):
    name = CharFilter(method='search_by_name')

    class Meta:
        model = Ingredients
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


class RecipesFilter(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_list = BooleanFilter(method='get_is_in_shopping_list')
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipes
        fields = ('author',)

    def get_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorites = self.request.user.favorites.all()
        return queryset.filter(
            pk__in=(favorite.recipes.pk for favorite in favorites)
        )

    def get_is_in_shopping_list(self, queryset, name, value):
        if not value:
            return queryset
        try:
            recipes = (
                self.request.user.shopping_list.recipes.all()
            )
        except Shopping_list.DoesNotExist:
            return queryset
        return queryset.filter(
            pk__in=(recipes.pk for recipe in recipes)
        )


class SearhIndigrients(FilterSet):
    name = CharFilter(method='search_by_name')

    class Meta:
        model = Ingredients
        fields = ('name',)

    def search_by_name(self, name):
        if not name:
            return ERROR_NAME
        return name.objects.all()