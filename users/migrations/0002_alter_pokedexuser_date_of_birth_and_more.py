# Generated by Django 5.0 on 2023-12-29 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokedexuser',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="pokedexuser",
            name="go_trainer_id",
            field=models.CharField(blank=True, default="", max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="pokedexuser",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="profile_pictures/"),
        ),
        migrations.AlterField(
            model_name="pokedexuser",
            name="trainer_qr_code",
            field=models.ImageField(blank=True, upload_to="trainer_qr_codes/"),
        ),
    ]
