from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Pokedex(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True  # Temporarily allow null values
                             )
    name = models.CharField(max_length=100, unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, null=True)
    cover_image = models.ImageField(upload_to='pokedex_covers/',
                                    blank=True,
                                    null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Pokedex)
def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class UserPokemon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True  # Temporarily allow null values
                             )
    pokedex = models.ForeignKey(Pokedex, on_delete=models.CASCADE)
    pokemon_id = models.IntegerField()
    pokemon_name = models.CharField(max_length=100, null=False)   # Temporarily allow null values
    is_favorite = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pokemon_id', 'pokedex')
