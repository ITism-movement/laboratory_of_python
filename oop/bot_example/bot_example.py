from telebot import TeleBot
from telebot.types import Message

from oop.bot_example.pokemon_client import PokeAPIClient

TOKEN = "<PLACE YOUR BOT TOKEN HERE>"


class PokemonBot(TeleBot):
    def __init__(self, poke_api_client: PokeAPIClient, token: str, *args, **kwargs):
        super().__init__(token=token, *args, **kwargs)
        self.poke_api_client = poke_api_client


# Create poke client
poke_api_client = PokeAPIClient(base_url='https://pokeapi.co/api/v2')

# Create bot with poke client
bot = PokemonBot(token=TOKEN, poke_api_client=poke_api_client)


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.reply_to(message, text="Welcome to Pokémon bot!")


@bot.message_handler(commands=["get_pokemons"])
def get_pokemon_list(message: Message):
    pokemons = bot.poke_api_client.get_pokemon_list(limit=10)
    result = "\n".join([f'🔹{pokemon_data["name"]}' for pokemon_data in pokemons["results"]])
    bot.send_message(chat_id=message.chat.id, text=result)


bot.polling()
