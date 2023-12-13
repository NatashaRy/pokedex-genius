# Generated by Django 5.0 on 2023-12-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_pokedexuser_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokedexuser",
            name="go_trainer_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="pokedexuser",
            name="trainer_qr_code",
            field=models.ImageField(
                blank=True, null=True, upload_to="trainer_qr_codes/"
            ),
        ),
    ]
