from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse, reverse_lazy
from .models import Pokedex, UserPokemon
import requests
from .forms import PokemonDropdown, PokedexForm, AddUserPokemonForm


@login_required
def dashboard(request):
    pokedexes = Pokedex.objects.filter(user=request.user)
    return render(request, 'pokedex/dashboard.html', {'pokedexes': pokedexes})


class PokedexCreateView(LoginRequiredMixin, CreateView):
    print('View is called')
    model = Pokedex
    form_class = PokedexForm
    template_name = 'pokedex/create_pokedex.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        color_value = form.cleaned_data['color']
        form.instance.color = color_value

        try:
            print('Form is valid')
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A Pokedex with this slug already exists.")
            print('Form is invalid')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('pokedex_details', kwargs={'slug': self.object.slug})


class PokedexDetailsView(LoginRequiredMixin, DetailView):
    print('Pokedex detailsView is called')
    model = Pokedex
    template_name = 'pokedex/pokedex_details.html'


class PokedexUpdateView(LoginRequiredMixin, UpdateView):
    model = Pokedex
    form_class = PokedexForm
    template_name = 'pokedex/update_pokedex.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PokedexDeleteView(LoginRequiredMixin, DeleteView):
    model = Pokedex
    slug_field = 'slug'
    success_url = reverse_lazy('dashboard')


class PokedexList(LoginRequiredMixin, ListView):
    model: Pokedex
    queryset = Pokedex.objects.order_by('-created_on')
    template_name = 'pokedex/dashboard.html'
    paginate_by = 9


@login_required
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


@login_required
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

    if request.method == 'POST':
        add_pokemon_form = AddUserPokemonForm(request.POST)
        if add_pokemon_form.is_valid():
            UserPokemon.objects.create(
                user=request.user,
                pokemon_id=entry_number,
                pokedex_id=request.objects.get('pokedex')
            )
            # Toast comfirmation message
    else:
        add_pokemon_form = AddUserPokemonForm()

    return render(request,
                  'pokedex/pokemon_details.html',
                  {'pokemon': pokemon_details,
                   'form': add_pokemon_form}
                  )











# @login_required
# class pokedex_list(generic.ListView):
#     model = Pokedex
#     queryset = Pokedex.objects.filter(status=1).order_by('-created_on')
#     template_name = 'pokedex/dashboard.html'
#     paginate_by = 9


# Characteristics
# Abilities: Each Pokémon may have one or more abilities that can affect battles and gameplay. Abilities can have various effects, such as boosting stats, preventing status conditions, or influencing weather.
# Stats: Pokémon have six core stats: HP (Hit Points), Attack, Defense, Special Attack, Special Defense, and Speed. These stats determine how well a Pokémon performs in battles and can be influenced by their species, level, and individual values (IVs).
# Evolution: Many Pokémon can evolve into a different species when they reach a certain level, meet specific conditions, or use certain items. Evolution can significantly impact a Pokémon's stats and appearance.
# Moves and Attacks: Pokémon can learn a variety of moves and attacks. The moves they know can be crucial in battles, and they can learn new moves as they level up or through other means.
# Egg Groups: Pokémon are categorized into different egg groups, which determine their breeding compatibility. Pokémon in the same egg group can breed to produce offspring.
# Pokedex Number: Each Pokémon has a unique Pokedex number that helps identify it within the game's Pokedex.
# Shiny Variation: Some Pokémon have a rare "shiny" variation with different coloration. Shiny Pokémon are highly sought after by collectors.
# Gigantamax/Dynamax Forms: In certain Pokémon games, some species can undergo Gigantamax or Dynamax transformations, granting them increased size and power in specific battles.
# Habitat: Pokémon can be found in various in-game habitats, such as forests, caves, or water bodies.
# Legendary and Mythical Pokémon: These are special, often unique, Pokémon with significant roles in the game's storyline.