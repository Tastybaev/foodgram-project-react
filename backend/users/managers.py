from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, email, login, password, **extra_fields):
        if not login:
            raise ValueError('Логин не может быть пустым!')
        if not email:
            raise ValueError('Почта не может быть пустой!')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, login, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError(
                'Суперпользователь должен быть is_superuser=True!'
            )
        return self.create_user(login, email, password, **extra_fields)
