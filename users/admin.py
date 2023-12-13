from django.contrib import admin
from .models import pokedexUser


class pokedexUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'date_of_birth')
    list_filter = ('date_joined',)
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)


admin.site.register(pokedexUser, pokedexUserAdmin)
