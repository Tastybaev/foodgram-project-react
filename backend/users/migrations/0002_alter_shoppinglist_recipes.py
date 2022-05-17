# Generated by Django 3.2.7 on 2022-05-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_tag_color'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipes',
            field=models.ManyToManyField(related_name='ShoppingList', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
    ]