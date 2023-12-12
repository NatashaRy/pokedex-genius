from django.contrib.auth.models import AbstractUser
from django.db import models


class pokedexUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    website_url = models.URLField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True, null=True
    )
