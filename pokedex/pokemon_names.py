import requests


def fetch_pokemon_names(limit=10):
    base_url = "https://pokeapi.co/api/v2/pokemon/"

    pokemon_names = []

    for i in range(1, limit + 1):
        response = requests.get(f"{base_url}{i}")
        if response.status_code == 200:
            data = response.json()
            name = data["name"]
            pokemon_names.append(name)
        else:
            print(f"Failed to fetch data for Pokémon {i}")

    return pokemon_names


if __name__ == "__main__":
    pokemon_limit = 30
    names = fetch_pokemon_names(limit=pokemon_limit)

    for index, name in enumerate(names, start=1):
        print(f"{index}. {name}")
