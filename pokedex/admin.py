from django.contrib import admin
from .models import Pokedex, UserPokemon


class PokedexAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'user', 'created_on', 'is_public')
    list_filter = ('is_public', 'created_on')
    search_fields = ('name', 'user__username')


class UserPokemonAdmin(admin.ModelAdmin):
    list_display = ('user', 'pokedex', 'pokemon_id', 'date_added', 'is_favorite')
    list_filter = ('pokedex', 'user')
    search_fields = ('pokedex__name', 'user__username')


admin.site.register(Pokedex, PokedexAdmin)
admin.site.register(UserPokemon, UserPokemonAdmin)
