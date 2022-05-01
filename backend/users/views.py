from django.db import IntegrityError
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView, UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from rest_framework.viewsets import GenericViewSet

from foodgram.pagination import LimitPageNumberPagination
from recipes.models import Recipes
from recipes.serializers.special import RecipesShortReadSerializer
from .models import Shoppinglist, Subscribe, User
from .serializers import SubscriptionSerializer


class TokenCreateWithCheckBlockStatusView(TokenCreateView):
    def _action(self, serializer):
        if serializer.user.is_blocked:
            return Response(
                {ERRORS_KEY: 'Данный аккаунт временно заблокирован!'},
                status=HTTP_400_BAD_REQUEST,
            )
        return super()._action(serializer)


class UserSubscribeViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
    lookup_url_kwarg = 'user_id'

    def get_subscribtion_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return SubscriptionSerializer(*args, **kwargs)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        self.get_serializer
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_subscribtion_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_subscribtion_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def create_subscribe(self, request, author):
        if request.user == author:
            return Response(
                {ERRORS_KEY: 'подписаться на себя запрещено!'},
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            subscribe = Subscribe.objects.create(
                user=request.user,
                author=author,
            )
        except IntegrityError:
            return Response(
                {ERRORS_KEY: 'Вы уже подписаны на этого автора!'},
                status=HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_subscribtion_serializer(subscribe.author)
        return Response(serializer.data, status=HTTP_201_CREATED) # возвращают контент автора.

    def delete_subscribe(self, request, author):
        try:
            Subscribe.objects.get(user=request.user, author=author).delete()
        except Subscribe.DoesNotExist:
            return Response(
                {ERRORS_KEY: 'Нельзя отписаться от неподписанного автора!'},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(
            status=HTTP_204_NO_CONTENT
        )

    @action(
        methods=('get', 'delete',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, user_id=None):
        try:
            author = get_object_or_404(User, pk=user_id)
        except Http404:
            return Response(
                {'detail': 'Пользователь не найден!'},
                status=HTTP_404_NOT_FOUND,
            )
        if request.method == 'GET':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)


class ShoppingListViewSet(GenericViewSet):
    NAME = 'ingredient_name'
    WEIGHT = 'ingredient_weight'
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipesShortReadSerializer
    queryset = Shoppinglist.objects.all()
    http_method_names = ('get', 'delete',)

    def generate_shopping_list_data(self, request):
        recipes = (
            request.user.Shoppinglist.recipes.prefetch_related('ingredients')
        )
        return (
            recipes.order_by(self.NAME)
            .values(self.NAME, self.WEIGHT)
            .annotate(total=Sum('ingredients__amount'))
        )

    def generate_ingredients_content(self, ingredients):
        content = ''
        for ingredient in ingredients:
            content += (
                f'{ingredient[self.NAME]}'
                f' ({ingredient[self.WEIGHT]})'
                f' — {ingredient["total"]}\r\n'
            )
        return content

    @action(detail=False)
    def download_shopping_list(self, request):
        try:
            ingredients = self.generate_shopping_list_data(request)
        except Shoppinglist.DoesNotExist:
            return Response(
                {ERRORS_KEY: 'Список покупок не существует!'},
                status=HTTP_400_BAD_REQUEST
            )
        content = self.generate_ingredients_content(ingredients)
        response = HttpResponse(
            content, content_type='text/plain,charset=utf8'
        )
        response['Content-Disposition'] = f'attachment; filename={FILE_NAME}'
        return response

    def add_to_shopping_list(self, request, Recipes, Shoppinglist):
        if Shoppinglist.recipes.filter(pk__in=(recipes.pk,)).exists():
            return Response(
                {ERRORS_KEY: 'Нельзя подписаться дважды!'},
                status=HTTP_400_BAD_REQUEST,
            )
        Shoppinglist.recipes.add(recipes)
        serializer = self.get_serializer(recipes)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def remove_from_shopping_list(self, request, Recipes, Shoppinglist):
        if not Shoppinglist.Recipes.filter(pk__in=(Recipes.pk,)).exists():
            return Response(
                {ERRORS_KEY: 'В списке покупок такого рецепта нет!'},
                status=HTTP_400_BAD_REQUEST,
            )
        Shoppinglist.recipes.remove(recipes)
        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    @action(methods=('get', 'delete',), detail=True)
    def shopping_list(self, request, pk=None):
        recipes = get_object_or_404(Recipes, pk=pk)
        shopping_list = (
            Shoppinglist.objects.get_or_create(user=request.user)[0]
        )
        if request.method == 'GET':
            return self.add_to_shopping_list(request, recipes, shopping_list)
        return self.remove_from_shopping_list(request, recipes, shopping_list)
