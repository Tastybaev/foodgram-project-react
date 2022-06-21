from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    SlugField,
    TextField,
    UniqueConstraint
)

from django.urls import reverse


User = get_user_model()

INGREDIENT_MIN_AMOUNT = 1
COOKING_TIME_MIN_VALUE = 1

COOKING_TIME_MIN_ERROR = (
    'Время приготовления не может быть меньше одной минуты!'
)
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиентов не может быть меньше {min_value}!'
)


class Tag(Model):
    name = CharField(max_length=255)
    color = CharField('Хекскод цвета', max_length=255)
    slug = SlugField('Слаг', max_length=255)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])


class Ingredient(Model):
    name = CharField(
        'Название ингредиента',
        max_length=255
    )
    measurement_unit = CharField(
        'Единица измерения',
        max_length=255
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class CountOfIngredient(Model):
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='count_in_recipes',
        verbose_name='Ингредиент',
    )
    amount = PositiveIntegerField(
        'Количество',
        validators=(MinValueValidator(
            INGREDIENT_MIN_AMOUNT,
            message=INGREDIENT_MIN_AMOUNT_ERROR.format(
                min_value=INGREDIENT_MIN_AMOUNT
            )
        ),)
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            UniqueConstraint(
                fields=('ingredient', 'amount',),
                name='unique_ingredient_amount',
            ),
        )

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.amount}'
            f' ({self.ingredient.measurement_unit})'
        )


class Recipe(Model):
    author = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = CharField(
        'Название',
        max_length=150
    )
    image = ImageField('Картинка')
    text = TextField('Описание')
    tags = ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    ingredients = ManyToManyField(
        'CountOfIngredient',
        related_name='recipes',
        verbose_name='Ингредиент',
    )
    cooking_time = PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(
            COOKING_TIME_MIN_VALUE,
            message=COOKING_TIME_MIN_ERROR,
        ),)
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.name} ({self.author})'

    def get_absoulute_url(self):
        return reverse('recipe', args=[self.pk])


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.recipe}'
