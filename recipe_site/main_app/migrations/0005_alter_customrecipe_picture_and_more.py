# Generated by Django 5.2 on 2025-05-02 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0004_alter_customrecipe_name_alter_premaderecipe_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customrecipe",
            name="picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="main_app/static/recipes"
            ),
        ),
        migrations.AlterField(
            model_name="premaderecipe",
            name="picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="main_app/static/recipes"
            ),
        ),
    ]
