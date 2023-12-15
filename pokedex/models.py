from django.db import models
from users.models import pokedexUser

STATUS = ((0, 'Draft'), (1, 'Published'))


class Pokedex(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    # featured_image = models.ImageField(upload_to='media/')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class UserPokemon(models.Model):
    user = models.ForeignKey(pokedexUser, on_delete=models.CASCADE)
    pokemon_id = models.IntegerField()
    pokedex_id = models.ForeignKey(Pokedex, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pokemon_id', 'pokedex_id')
