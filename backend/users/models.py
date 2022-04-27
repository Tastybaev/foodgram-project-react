from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import *

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    login = CharField(max_length=25)
    password = CharField(max_length=25)
    email = EmailField(help_text='email address', unique=True)
    first_name = CharField(max_length=25)
    last_name = CharField(max_length=25 )
    is_superuser = BooleanField('Администратор', default=False)
    is_blocked = BooleanField('Заблокирован', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'login', 'password',  'email', 'first_name', 'last_name',
    ]

    objects = UserManager()

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'  

    def __str__(self):
        return self.login

    @property
    def is_staff(self):
        return self.is_superuser


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


class Shoppinglist(Model):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    recipes = ManyToManyField(
        'recipes.Recipes',
        related_name='in_shopping_list',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}'