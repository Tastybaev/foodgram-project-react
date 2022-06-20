# Generated by Django 3.2.7 on 2022-06-20 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_shoppingcart_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user',), name='unique_user'),
        ),
    ]
