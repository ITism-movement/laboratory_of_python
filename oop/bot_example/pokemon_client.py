import requests
from typing import Any


class PokeAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_pokemon_list(self, limit: int = 100, offset: int = 0) -> dict[Any, Any]:
        """Get a list of Pokémon with optional pagination."""
        endpoint = f'/pokemon?limit={limit}&offset={offset}'
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_pokemon_by_id(self, pokemon_id: int) -> dict[Any, Any]:
        """Get details of a Pokémon by its ID."""
        endpoint = f'/pokemon/{pokemon_id}'
        response = requests.get(self.base_url + endpoint)
        return response.json()
