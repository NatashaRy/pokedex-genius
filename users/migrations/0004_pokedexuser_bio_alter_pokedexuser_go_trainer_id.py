# Generated by Django 5.0 on 2023-12-13 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_pokedexuser_go_trainer_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokedexuser",
            name="bio",
            field=models.TextField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name="pokedexuser",
            name="go_trainer_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]