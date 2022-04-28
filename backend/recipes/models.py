from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import *

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
    name = CharField(max_length=50)
    color = CharField('Хекскод цвета', max_length=7)
    slug = SlugField('Слаг', max_length=200)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])


class Ingredients(Model):
    name = CharField('Название ингредиента',
       max_length=50
    ),
    weight = CharField('Единица измерения',
        max_length=50
    )
    class Meta:
        verbose_name = 'ingredients'
        verbose_name_plural = 'ingredients'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'

class CountOfIngredients(Model):
    ingredients = ForeignKey(
        Ingredients,
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
                fields=('ingredients', 'amount',),
                name='unique_ingredient_amount',
            ),
        )

    def __str__(self):
        return (
            f'{self.ingredients.name} - {self.amount}'
            f' ({self.ingredients.weight})'
        )


class Recipes(Model):
    author = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = CharField('Название',
       max_length=150
    )
    image = ImageField('Картинка')
    text = TextField('Описание')
    tags = ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    ingredient = ManyToManyField(
        CountOfIngredients,
        related_name='count_in_recipes',
        verbose_name='Ингредиент',
    )
    cooking_time = PositiveIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(
            COOKING_TIME_MIN_VALUE,
            message=COOKING_TIME_MIN_ERROR,
        ),)
    )

    def __str__(self):
        return f'{self.name} ({self.author})'

    def get_absoulute_url(self):
        return reverse('recipes', args=[self.pk])


class Favorite(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipes = ForeignKey(
        Recipes,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipes',),
                name='unique_user_recipes',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.recipes}'
