from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.urls import reverse, reverse_lazy
from .models import Pokedex, UserPokemon
import requests
from .forms import PokemonDropdown, PokedexForm, AddUserPokemonForm


class UserIsOwnerMixin:
    """
    Only let the user who owns the object access it
    """
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def dashboard(request):
    """
    Only let signed-in users access the dashboard with
    their Pokedexes and favorite Pokemons.
    Count Pokemon in Pokedexes and favorite Pokemon
    """
    pokedexes = Pokedex.objects.filter(
        user=request.user).annotate(num_pokemon=Count('userpokemon'))

    favorite_pokemons = UserPokemon.objects.filter(
        user=request.user, is_favorite=True)
    favorite_pokemons_count = favorite_pokemons.count()

    return render(request, 'pokedex/dashboard.html', {
        'pokedexes': pokedexes,
        'favorite_pokemons': favorite_pokemons,
        'favorite_pokemons_count': favorite_pokemons_count
    })


class PokedexCreateView(LoginRequiredMixin, CreateView):
    """
    Only let signed-in users create Pokedexes, user can favorize Pokedexes
    Validats if a the name of the Pokedex already exists
    """
    model = Pokedex
    form_class = PokedexForm
    template_name = 'pokedex/pokedex_create.html'

    def form_valid(self, form):
        form.save()
        form.instance.user = self.request.user
        color_value = form.cleaned_data['color']
        form.instance.color = color_value

        form.instance.is_favorite = form.cleaned_data.get('is_favorite')

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A Pokedex with this slug already exists.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('pokedex_details', kwargs={'slug': self.object.slug})


class PokedexDetailsView(LoginRequiredMixin, DetailView):
    """
    Let signed-in users access the details of their Pokedexes, shows
    the number of Pokemon in the Pokedex let the user edit the Pokedex
    """
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
    """
    Let signed-in users edit the details of their Pokedex
    """
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
    """
    Let signed-in users who owns the Pokedex to delete it
    """
    model = Pokedex
    slug_field = 'slug'
    template_name = 'pokedex/pokedex_delete.html'
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Pokedex successfully deleted.')
        return super().delete(request, *args, **kwargs)


class PokemonDeleteView(UserIsOwnerMixin, DeleteView):
    """
    Let signed-in users who owns the Pokemon to delete it from a Pokedex
    """
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
    """
    Displays all Pokedexes of the signed-in user, 9 Pokedexes per page
    """
    model: Pokedex
    queryset = Pokedex.objects.order_by('-created_on')
    template_name = 'pokedex/dashboard.html'
    paginate_by = 9


@login_required
def search(request):
    """
    Signed-in users can search for Pokemon in a dropdown menu
    """
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
    """
    Signed-in users get information about chosen Pokemon
    and can add Pokemon to their Pokedex
    """
    try:
        response = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{entry_number}/')
        response.raise_for_status()
        pokemon_data = response.json()
        pokemon_name = pokemon_data.get("name", "")
    except requests.exceptions.HTTPError as e:
        error_message = f'Failed to fetch Pokemon details. Error: {
            e.response.status_code} {e.response.reason}'
        messages.error(request, error_message)
        return redirect('search')

    form = AddUserPokemonForm(user=request.user)

    if request.method == 'POST':
        form = AddUserPokemonForm(
            data=request.POST,
            user=request.user,
            initial={"pokemon_name": pokemon_name}
        )
        if form.is_valid():
            new_user_pokemon = form.save(commit=False)
            new_user_pokemon.user = request.user
            new_user_pokemon.pokemon_id = request.POST.get(
                'entry_number',
                entry_number
            )
            new_user_pokemon.pokemon_name = pokemon_name

            if UserPokemon.objects.filter(
                pokemon_id=new_user_pokemon.pokemon_id,
                pokedex=new_user_pokemon.pokedex
            ).exists():
                form.add_error(None,
                               'This Pokemon is already in '
                               'the selected Pokedex.')
            else:
                new_user_pokemon.save()
                return redirect('pokedex_details',
                                slug=form.instance.pokedex.slug)

    return render(request, 'pokedex/pokemon_details.html', {
        'pokemon': pokemon_data,
        'form': form,
    })
