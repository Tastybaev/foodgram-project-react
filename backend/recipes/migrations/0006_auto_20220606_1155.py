# Generated by Django 3.2.7 on 2022-06-06 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'ingredient', 'verbose_name_plural': 'ingredients'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='recipes.CountOfIngredient', verbose_name='Ингредиент'),
        ),
    ]