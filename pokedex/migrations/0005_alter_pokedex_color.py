# Generated by Django 5.0 on 2023-12-18 16:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokedex", "0004_alter_pokedex_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokedex",
            name="color",
            field=models.CharField(max_length=7, null=True),
        ),
    ]
