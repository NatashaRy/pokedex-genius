# Generated by Django 5.0 on 2023-12-30 13:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_pokedexuser_profile_picture_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pokedexuser",
            name="profile_picture",
        ),
        migrations.RemoveField(
            model_name="pokedexuser",
            name="trainer_qr_code",
        ),
        migrations.AlterField(
            model_name="pokedexuser",
            name="go_trainer_id",
            field=models.CharField(blank=True, default=None, max_length=255),
        ),
    ]
