from django.contrib import admin
from .models import Pokedex


class PokedexAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'user', 'created_on', 'is_public')
    list_filter = ('is_public', 'created_on')
    search_fields = ('name', 'user__username')


admin.site.register(Pokedex, PokedexAdmin)
