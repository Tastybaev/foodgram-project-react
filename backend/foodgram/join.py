from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from recipes.models import Recipe
from users.models import ShoppingCart


def food_staff_add(self, request, recipe, shopping_cart):
    return Response(
        {ERRORS_KEY: 'Нельзя подписаться дважды!'},
        status=HTTP_400_BAD_REQUEST,
    )

def food_staff_remove(self, request, recipe, shopping_cart):
    return Response(
        {ERRORS_KEY: 'Данных по данному запросу не существует!'},
        status=HTTP_400_BAD_REQUEST,
    )
