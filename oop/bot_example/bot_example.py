from telebot import TeleBot
from telebot.types import Message
import os

from oop.bot_example.pokemon_client import PokeAPIClient, PokeAPIClientService

# you can create your own bot via Telegram BotFather
TOKEN = ""


class PokemonBot(TeleBot):
    def __init__(self,
                 poke_api_client: PokeAPIClient,
                 poke_api_client_service: PokeAPIClientService,
                 token: str,
                 *args, **kwargs):
        super().__init__(token=token, *args, **kwargs)
        self.poke_api_client = poke_api_client
        self.poke_api_client_service = poke_api_client_service


# Create poke client
poke_api_client = PokeAPIClient(base_url='https://pokeapi.co/api/v2')
poke_api_client_service = PokeAPIClientService(base_url='https://pokeapi.co/api/v2',
                                               secret_token="SOME_TOKEN_VALUE",
                                               # secret_token=os.getenv("SECRET")
                                               )

# Create bot with poke client
bot = PokemonBot(token=TOKEN, poke_api_client=poke_api_client, poke_api_client_service=poke_api_client_service)


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.reply_to(message, text="Welcome to Pokémon bot!")


@bot.message_handler(commands=["get_pokemons"])
def get_pokemon_list(message: Message):
    pokemons = bot.poke_api_client.get_pokemon_list(limit=10)
    result = "\n".join([f'🔹{pokemon_data["name"]}' for pokemon_data in pokemons["results"]])
    bot.send_message(chat_id=message.chat.id, text=result)


@bot.message_handler(commands=["get_metrics"])
def get_metrics(message: Message):
    secret_token_from_user = message.text.split()[1]
    result = bot.poke_api_client_service.get_service_metric(secret_token=secret_token_from_user)
    bot.send_message(chat_id=message.chat.id, text=result)


bot.polling()
