from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import ShoppingList, User


@receiver(post_save, sender=User)
def create_shopping_list(sender, instance, created, **kwargs):
    if created:
        ShoppingList.objects.create(user=instance)


@receiver(post_save, sender=User)
def destroy_token(sender, instance, created, **kwargs):
    if created or not instance.is_blocked:
        return
    token = Token.objects.filter(user=instance)
    if token.exists():
        token.first().delete()