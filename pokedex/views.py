from django.shortcuts import render, redirect
from django.views import generic
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
        choices = [(pokemon['entry_number'],
                    pokemon['pokemon_species']['name'].
                    title()) for pokemon in pokemon_entries]
    except requests.exceptions.HTTPError as e:
        print(e)
        choices = []

    if request.method == 'POST':
        form = PokemonDropdown(data=request.POST, choices=choices)
        if form.is_valid():
            entry_number = form.cleaned_data['pokemon']
            return redirect('pokemon_details', entry_number=entry_number)
        else:
            form = PokemonDropdown(choices=choices)
            print('Form is invalid')
            print(form.errors)  # Print form errors for debugging
    else:
        form = PokemonDropdown(choices=choices)

    return render(request, 'pokedex/search.html', {'form': form})


def pokemon_details(request, entry_number):
    try:
        response = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{entry_number}/'
            )
        response.raise_for_status()
        print('Requests pokemon entry number', entry_number)    # Debug print
        pokemon_details = response.json()

    except requests.exceptions.HTTPError as e:
        print(e)
        pokemon_details = {}

    return render(request,
                  'pokedex/pokemon_details.html',
                  {'pokemon': pokemon_details}
                  )


class PokedexList(generic.ListView):
    model = Pokedex
    queryset = Pokedex.objects.filter(status=1).order_by('-created_on')
    template_name = 'pokedex/dashboard.html'
    paginate_by = 9
