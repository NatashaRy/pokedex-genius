from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from .models import Pokedex
import requests
from .forms import PokemonDropdown


def dashboard(request):
    return render(request, 'pokedex/dashboard.html')


def search(request):
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokedex/1')
        response.raise_for_status()
        data = response.json()

        pokemon_entries = data.get('pokemon_entries', [])
        choices = [(
            pokemon['pokemon_species']['name'],
            pokemon['pokemon_species']['name'].
            title()) for pokemon in pokemon_entries]

        form = PokemonDropdown(choices=choices)

    except requests.exceptions.HTTPError as e:
        print(e)
        form = PokemonDropdown(choices=[])

    return render(request, 'pokedex/search.html', {'form': form})

# def pokemon_data_view(request):
#     pokemon_id = request.GET.get('id')
#     data = get_pokemon_data(pokemon_id)
#     if data is None:
#         return JsonResponse({'error': 'Error fetching data'}, status=500)
#     return JsonResponse(data)


# def pokemon_view(request):
#     region = request.GET.get('region', '')
#     pokemons = get_pokemons(region)
    return JsonResponse({'pokemons': pokemons})


# def pokemon_detail(request, pokemon_name):
#     pokemon = get_data(pokemon_name)
#     if pokemon:
#         return render(request,
#                       'pokedex/pokemon_detail.html', {
#                           'pokemon': pokemon})
#     else:
#         return render(request, 'pokedex/pokemon_not_found.html')


class PokedexList(generic.ListView):
    model = Pokedex
    queryset = Pokedex.objects.filter(status=1).order_by('-created_on')
    template_name = 'pokedex/dashboard.html'
    paginate_by = 9
