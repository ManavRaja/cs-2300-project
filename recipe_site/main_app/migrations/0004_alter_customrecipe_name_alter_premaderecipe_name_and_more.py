# Generated by Django 5.2 on 2025-05-01 05:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0003_alter_customrecipe_name_alter_premaderecipe_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="customrecipe",
            name="name",
            field=models.CharField(default="My Recipe Name", max_length=200),
        ),
        migrations.AlterField(
            model_name="premaderecipe",
            name="name",
            field=models.CharField(default="My Recipe Name", max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name="customrecipe",
            unique_together={("user", "name")},
        ),
    ]
