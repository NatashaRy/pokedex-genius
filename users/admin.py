from django.contrib import admin
from .models import pokedexUser


class pokedexUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'date_of_birth', 'website_url', 'bio', 'go_trainer_id', 'trainer_qr_code', 'profile_picture', 'date_joined', 'last_login')
    list_filter = ('date_joined', 'last_login')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    def last_login(self, obj):
        return obj.last_login.strftime("%d-%m-%Y %H:%M:%S")

    last_login.admin_order_field = 'last_login'
    last_login.short_description = 'Last Login'


admin.site.register(pokedexUser, pokedexUserAdmin)
