from .models import Pokedex


# Function acts as a context processor for Django templates.
# It checks if a user is authenticated and, if so, retrieves all
# Pokedex instances associated with the authenticated user from the database.
def user_pokedexes(request):
    if request.user.is_authenticated:
        pokedexes = Pokedex.objects.filter(user=request.user)
        return {'user_pokedexes': pokedexes}
    return {}
