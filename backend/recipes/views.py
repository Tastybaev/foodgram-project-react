from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from foodgram.join import food_staff_add, food_staff_remove
from foodgram.mixins import ListRetriveViewSet
from foodgram.pagination import LimitPageNumberPagination
from foodgram.permissions import IsAuthorOrAdminOrReadOnly
from .filters import IngredientSearchFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, Tag
from .serializers.general import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer
)
from .serializers.special import RecipeShortReadSerializer

ERRORS_KEY = 'errors'


class TagViewSet(ListRetriveViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    http_method_names = ('get',)


class IngredientViewSet(ListRetriveViewSet):
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    queryset = Ingredient.objects.all()
    http_method_names = ('get',)


class RecipeViewSet(ModelViewSet):
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'put', 'patch', 'delete',)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_to_favorite(self, request, recipe):
        try:
            Favorite.objects.create(user=request.user, recipe=recipe)
        except IntegrityError:
            return food_staff_add(request, recipe, True)
        serializer = RecipeShortReadSerializer(recipe)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def delete_from_favorite(self, request, recipe):
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if not favorite.exists():
            return food_staff_remove(request, recipe, False)

    @action(
        methods=('get', 'post', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'GET':
            return self.delete_from_favorite(request, recipe)
        return self.add_to_favorite(request, recipe)
