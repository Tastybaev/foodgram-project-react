from rest_framework.serializers import ModelSerializer

from recipes.models import Recipes


class RecipesShortReadSerializer(ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'
