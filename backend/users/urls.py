from django.urls import include, path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (
    ShoppingListViewSet,
    TokenCreateWithCheckBlockStatusView,
    UserSubscribeViewSet
)

router = DefaultRouter()

router.register(r'users', UserSubscribeViewSet, basename='users')
router.register(r'recipes', ShoppingListViewSet, basename='shopping_list')

app_name = 'users'

auth_patterns = [
    path(
        'token/login/',
        TokenCreateWithCheckBlockStatusView.as_view(),
        name="login",
    ),
    path(
        'token/logout/', 
        TokenDestroyView.as_view(), 
        name="logout"
    ),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
