import requests
from typing import Any


def get_pokemon_list(base_url: str, limit: int = 100, offset: int = 0) -> dict[Any, Any]:
    """Get a list of Pokémon with optional pagination."""
    endpoint = f'{base_url}/pokemon?limit={limit}&offset={offset}'
    response = requests.get(endpoint)
    return response.json()


class PokeAPIClient:
    def __init__(self, base_url: str):
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


class PokeAPIClientService(PokeAPIClient):
    def __init__(self, base_url: str, secret_token: str):
        super().__init__(base_url=base_url)
        self.secret_token = secret_token

    def get_service_metric(self, secret_token: str):
        if self.secret_token == secret_token:
            return "Some sensitive data"
        else:
            return "Invalid TOKEN"
