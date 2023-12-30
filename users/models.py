from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None,
                         password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class pokedexUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    website_url = models.URLField(blank=True)
    bio = models.TextField(max_length=150, blank=True)
    go_trainer_id = models.CharField(max_length=255,
                                     blank=True,
                                     default=None,
                                     null=True)

    objects = CustomUserManager()
