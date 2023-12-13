from django.shortcuts import render
from django.views import generic
from .models import Pokedex
from .forms import PokemonSearchForm
from .pokeapi import get_data


def dashboard(request):
    return render(request, 'pokedex/dashboard.html')


def search_pokemon(request):
    form = PokemonSearchForm(request.GET or None)
    pokemon_data = None
    search_performed = False
    pokemon_names = []

    if 'query' in request.GET and form.is_valid():
        search_performed = True
        query = form.cleaned_data['query']

        selected_pokemon = request.GET.get(
            'selected_pokemon'
            )

        for i in range(1, 11):
            pokemon_names.append(f"Pokemon {i}")

    return render(request, 'pokedex/search.html', {
        'form': form,
        'pokemon_data': pokemon_data,
        'search_performed': search_performed,
        'query': query if search_performed else "",
        'pokemon_names': pokemon_names,
    })


def pokemon_detail(request, pokemon_name):
    pokemon = get_data(pokemon_name)
    if pokemon:
        return render(request,
                      'pokedex/pokemon_detail.html', {
                          'pokemon': pokemon})
    else:
        return render(request, 'pokedex/pokemon_not_found.html')


class PokedexList(generic.ListView):
    model = Pokedex
    queryset = Pokedex.objects.filter(status=1).order_by('-created_on')
    template_name = 'pokedex/dashboard.html'
    paginate_by = 9
