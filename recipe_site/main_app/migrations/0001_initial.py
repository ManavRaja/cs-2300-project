# Generated by Django 5.2 on 2025-04-30 02:03

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PremadeRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("instructions", models.TextField(blank=True, null=True)),
                (
                    "picture",
                    models.ImageField(blank=True, null=True, upload_to="recipes/"),
                ),
                ("protein", models.PositiveIntegerField(blank=True, null=True)),
                ("calories", models.PositiveIntegerField(blank=True, null=True)),
                ("fat", models.PositiveIntegerField(blank=True, null=True)),
                ("carbohydrates", models.PositiveIntegerField(blank=True, null=True)),
                ("ingredients", models.TextField(blank=True, null=True)),
                (
                    "cook_time",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("cuisine", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("instructions", models.TextField(blank=True, null=True)),
                (
                    "picture",
                    models.ImageField(blank=True, null=True, upload_to="recipes/"),
                ),
                ("protein", models.PositiveIntegerField(blank=True, null=True)),
                ("calories", models.PositiveIntegerField(blank=True, null=True)),
                ("fat", models.PositiveIntegerField(blank=True, null=True)),
                ("carbohydrates", models.PositiveIntegerField(blank=True, null=True)),
                ("ingredients", models.TextField(blank=True, null=True)),
                (
                    "cook_time",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("cuisine", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="custom_recipes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WeeklyMealPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                (
                    "recipes",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="meal_plans",
                        to="main_app.customrecipe",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="meal_plans",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "start_date")},
            },
        ),
    ]
