# Generated by Django 5.0 on 2023-12-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokedex", "0011_alter_pokedex_cover_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokedex",
            name="cover_image",
            field=models.ImageField(blank=True, null=True, upload_to="pokedex_covers/"),
        ),
    ]