from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipesViewSet, TagViewSet

router = DefaultRouter()
router.register(r'Tag', TagViewSet, basename='tags')
router.register(r'Ingredients', IngredientViewSet, basename='ingredients')
router.register(r'Recipes', RecipeViewSet, basename='recipes')

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]