import os

import telebot  # pip install pytelegrambotapi
from telebot import types

# Инициализация бота
API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN)


# Функция для создания клавиатуры с кнопками
def get_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button_1")
    button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button_2")
    keyboard.add(button1, button2)
    return keyboard


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=get_keyboard())


# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "button_1":
        new_text = "Вы нажали на Кнопку 1!"
    elif call.data == "button_2":
        new_text = "Вы нажали на Кнопку 2!"

    # Редактирование сообщения
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=new_text,
                          )  # Оставляем ту же клавиатуру для повторного выбора


# Запуск бота
bot.polling(none_stop=True)
