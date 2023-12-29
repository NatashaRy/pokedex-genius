from django.contrib.auth.models import AbstractUser
from django.db import models


class pokedexUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    website_url = models.URLField(blank=True)
    bio = models.TextField(max_length=150, blank=True)
    go_trainer_id = models.CharField(max_length=20, blank=True,
                                     default='123412341234')
    trainer_qr_code = models.ImageField(upload_to='trainer_qr_codes/',
                                        blank=True,
                                        default='static/images/trainer-qr-code.webp')
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True,
                                        default='static/images/pikachu-placeholder.webp')