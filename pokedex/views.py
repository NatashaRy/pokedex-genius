from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse, reverse_lazy
from .models import Pokedex, UserPokemon
import requests
from .forms import PokemonDropdown, PokedexForm, AddUserPokemonForm


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def dashboard(request):
    pokedexes = Pokedex.objects.filter(
        user=request.user).annotate(
        num_pokemon=Count('userpokemon')
        )

    return render(request, 'pokedex/dashboard.html', {'pokedexes': pokedexes})


class PokedexCreateView(LoginRequiredMixin, CreateView):
    model = Pokedex
    form_class = PokedexForm
    template_name = 'pokedex/pokedex_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        color_value = form.cleaned_data['color']
        form.instance.color = color_value

        form.instance.is_favorite = form.cleaned_data.get('is_favorite')

        try:
            print('Form is valid')  # debugging
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A Pokedex with this slug already exists.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('pokedex_details', kwargs={'slug': self.object.slug})


class PokedexDetailsView(LoginRequiredMixin, DetailView):
    model = Pokedex
    template_name = 'pokedex/pokedex_details.html'
    context_object_name = 'pokedex'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokedex = self.get_object()
        context['pokemons'] = UserPokemon.objects.filter(pokedex=pokedex)
        context['num_pokemon'] = context['pokemons'].count()
        return context


class PokedexUpdateView(LoginRequiredMixin, UpdateView):
    model = Pokedex
    form_class = PokedexForm
    template_name = 'pokedex/pokedex_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_favorite = form.cleaned_data.get('is_favorite')
        return super().form_valid(form)

    def get_success_url(self):
        updated_pokedex_slug = self.object.slug
        return reverse('pokedex_details',
                       kwargs={'slug': updated_pokedex_slug})


class PokedexDeleteView(UserIsOwnerMixin, DeleteView):
    model = Pokedex
    slug_field = 'slug'
    template_name = 'pokedex/pokedex_delete.html'
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Pokedex successfully deleted.')
        return super().delete(request, *args, **kwargs)


class PokemonDeleteView(UserIsOwnerMixin, DeleteView):
    model = UserPokemon
    pk_url_kwarg = 'pokemon_id'
    template_name = 'pokedex/pokemon_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pokemon'] = self.get_object()
        context['pokedex'] = context['pokemon'].pokedex
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['pokemon'] = self.get_object()
        context['pokedex'] = context['pokemon'].pokedex
        return self.render_to_response(context)

    def get_success_url(self):
        messages.success(self.request,
                         'Pokemon successfully removed from Pokedex.')
        return reverse_lazy('pokedex_details',
                            kwargs={'slug': self.kwargs['pokedex_slug']})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Pokemon successfully deleted.')
        return super().delete(request, *args, **kwargs)


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
    else:
        form = PokemonDropdown(choices=choices)

    return render(request, 'pokedex/search.html', {'form': form})


@login_required
def pokemon_details(request, entry_number):
    print(f"Received entry number (parameter): {entry_number}")              # Debugging

    try:
        response = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{entry_number}/'
        )
        response.raise_for_status()
        pokemon_data = response.json()

        # Extract the name of the Pokemon from the API response
        pokemon_name = pokemon_data.get("name", "")
    except requests.exceptions.HTTPError as e:
        print(f'Error fetching Pokemon details: {e}')                            # Debugging
        messages.error(request, 'Failed to fetch Pokemon details.')
        return redirect('search')

    form = AddUserPokemonForm(user=request.user)

    if request.method == 'POST':
        # Populate the "pokemon_name" field with the extracted name
        form = AddUserPokemonForm(
            data=request.POST,
            user=request.user,
            initial={"pokemon_name": pokemon_name}  # Initialize the field
        )
        print(f"Form data (POST): {request.POST}")                       # Debugging

        if form.is_valid():
            print('Form is valid')                                  # Debugging
            new_user_pokemon = form.save(commit=False)
            new_user_pokemon.user = request.user
            new_user_pokemon.pokemon_id = request.POST.get(
                'entry_number',
                entry_number
            )
            new_user_pokemon.pokemon_name = pokemon_name
            print(f'Form fields entry number: {new_user_pokemon.pokemon_id}')                           # Debugging

            if UserPokemon.objects.filter(
                pokemon_id=new_user_pokemon.pokemon_id,
                pokedex=new_user_pokemon.pokedex
            ).exists():
                form.add_error(None, 'This Pokemon is already in the selected Pokedex.')
            else:
                new_user_pokemon.save()
                return redirect('pokedex_details', slug=form.instance.pokedex.slug)
        else:
            print('Form errors:', form.errors)                  # Debugging
    else:
        print('GET request, no form data')                  # Debugging

    return render(request, 'pokedex/pokemon_details.html', {
        'pokemon': pokemon_data,
        'form': form,
    })



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