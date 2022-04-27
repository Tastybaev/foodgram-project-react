from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import *

from recipes.models import *
from users.models import Shoppinglist
from users.serializers import UserSerializer

TAGS_UNIQUE_ERROR = 'Теги не могут повторяться!'
TAGS_EMPTY_ERROR = 'Рецепт не может быть без тегов!'
INGREDIENTS_UNIQUE_ERROR = 'Ингредиенты не могут повторяться!'
INGREDIENTS_EMPTY_ERROR = 'Без ингредиентов рецепта не бывает!'
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиента не может быть меньше {min_value}!'
)
INGREDIENT_DOES_NOT_EXIST = 'Такого ингредиента не существует!'

INGREDIENT_MIN_AMOUNT = 1
COOKING_TIME_MIN_VALUE = 1

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit',)


class RecipesIngredientWriteSerializer(ModelSerializer):
    class Meta:
        model = CountOfIngredients
        fields = ('id', 'amount',)
        extra_kwargs = {
            'id': {
                'read_only': False,
                'error_messages': {
                    'does_not_exist': INGREDIENT_DOES_NOT_EXIST,
                }
            },
            'amount': {
                'error_messages': {
                    'min_value': INGREDIENT_MIN_AMOUNT_ERROR.format(
                        min_value=INGREDIENT_MIN_AMOUNT
                    ),
                }
            }
        }


class RecipesIngredientReadSerializer(ModelSerializer):
    id = IntegerField(source='ingredient.id')
    name = CharField(source='ingredient.name')
    measurement_unit = CharField(source='ingredient.measurement_unit')

    class Meta:
        model = CountOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipesReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipesIngredientReadSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_list = SerializerMethodField()

    class Meta:
        model = Recipes
        fields = '__all__'

    def get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, obj):
        user = self.get_user()
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_list(self, obj):
        user = self.get_user()
        try:
            return (
                user.is_authenticated and
                user.Shoppinglist.Recipes.filter(pk__in=(obj.pk,)).exists()
            )
        except Shoppinglist.DoesNotExist:
            return False


class RecipesWriteSerializer(ModelSerializer):
    ingredients = RecipesIngredientWriteSerializer(many=True)
    tags = ListField(
        child=SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all(),
        ),
    )
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )
        extra_kwargs = {
            'cooking_time': {
                'error_messages': {
                    'min_value': COOKING_TIME_MIN_ERROR,
                }
            }
        }

    def validate(self, attrs):
        if attrs['cooking_time'] < COOKING_TIME_MIN_VALUE:
            raise ValidationError(COOKING_TIME_MIN_ERROR)
        if len(attrs['tags']) == 0:
            raise ValidationError(TAGS_EMPTY_ERROR)
        if len(attrs['tags']) > len(set(attrs['tags'])):
            raise ValidationError(TAGS_UNIQUE_ERROR)
        if len(attrs['ingredients']) == 0:
            raise ValidationError(INGREDIENTS_EMPTY_ERROR)
        id_ingredients = []
        for ingredient in attrs['ingredients']:
            if ingredient['amount'] < INGREDIENT_MIN_AMOUNT:
                raise ValidationError(
                    INGREDIENT_MIN_AMOUNT_ERROR.format(
                        min_value=INGREDIENT_MIN_AMOUNT,
                    )
                )
            id_ingredients.append(ingredient['id'])
        if len(id_ingredients) > len(set(id_ingredients)):
            raise ValidationError(INGREDIENTS_UNIQUE_ERROR)
        return attrs

    def add_ingredients_and_tags(self, instance, validated_data):
        ingredients, tags = (
            validated_data.pop('ingredients'), validated_data.pop('tags')
        )
        for ingredient in ingredients:
            count_of_ingredients, _ = CountOfIngredients.objects.get_or_create
            (
                ingredient=get_object_or_404(Ingredient, pk=ingredient['id']),
                amount=ingredient['amount'],
            )
            instance.ingredients.add(count_of_ingredients)
        for tag in tags:
            instance.tags.add(tag)
        return instance

    def create(self, validated_data):
        saved = {}
        saved['ingredients'] = validated_data.pop('ingredients')
        saved['tags'] = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        return self.add_ingredients_and_tags(recipe, saved)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.add_ingredients_and_tags(instance, validated_data)
        return super().update(instance, validated_data)


class RecipesShortReadSerializer(ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'