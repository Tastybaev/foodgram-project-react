# import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    login = models.Charfield(
       max_length=25
    ),
    password = models.Charfield(
       max_length=25 
    ),
    email = models.EmailField(
        help_text='email address',
        unique=True,
    ),
    first_name = models.Charfield(
       max_length=25 
    ),
    last_name = models.Charfield(
       max_length=25 
    )

    class Userlevel:
        USER = 'user'
        ADMIN = 'admin'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
        ]

    level = models.CharField(
        max_length=25,
        choices=Userlevel.choices,
        default=Userlevel.USER,
    )
    # confirmation_code = models.UUIDField(
    #     default=uuid.uuid4,
    #     editable=False,
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login', 'password',  'email', 'first_name', 'last_name']

    class Meta:
        ordering = ('-pk',)


class Subscribe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscribe',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.author}'


class Shopping_list(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    recipes = ForeignKey(
        'recipes.Recipe',
        related_name='in_shopping_list',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}'