from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe


class RecipeShortReadSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
