from pokebase import cache
import requests


cache.API_CACHE = True
cache.API_CACHE_EXPIRE_SECONDS = 86400  # 24 hours


def get_pokemon_by_region(region_name):
    url = f'https://pokeapi.co/api/v2/pokedex/{region_name}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['pokemon_entries']
    except requests.exceptions.HTTPError as e:
        print(f'Error fetching data: {e}')
        return None


def get_pokemons(region):
    pokemons = get_pokemon_by_region(region)
    if pokemons is None:
        return {'error': 'Error fetching data'}
    return pokemons


def get_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.HTTPError as e:
        print(f'Error fetching data: {e}')
        return {'error': 'Error fetching data'}
