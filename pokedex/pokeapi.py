import pokebase as pb
from pokebase import cache

cache.API_CACHE = True
cache.API_CACHE_EXPIRE_SECONDS = 86400  # 24 hours


def get_data(pokemon_name):
    try:
        pokemon = pb.pokemon(pokemon_name)
        return {
            'name': pokemon.name,
            'order': pokemon.order,
            'sprites': {
                'front_default': pokemon.sprites.front_default
            },
            'types': [{'type': {'name': t.type.name}} for t in pokemon.types]
        }
    except ValueError:
        return None
