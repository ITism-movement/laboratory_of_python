import telebot
from telebot import types
import os

# Инициализация бота
API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Создадим список данных для демонстрации (например, список товаров)
items = [f"Товар {i}" for i in range(1, 22)]  # 20 товаров

# Количество элементов на одной странице
ITEMS_PER_PAGE = 5


# Функция для создания клавиатуры с кнопками "Назад" и "Вперед"
def get_pagination_keyboard(current_page, total_pages):
    keyboard = types.InlineKeyboardMarkup()
    if current_page > 1:
        prev_button = types.InlineKeyboardButton("Назад", callback_data=f"page_{current_page - 1}")
        keyboard.add(prev_button)
    if current_page < total_pages:
        next_button = types.InlineKeyboardButton("Вперед", callback_data=f"page_{current_page + 1}")
        keyboard.add(next_button)
    return keyboard


# Функция для отображения элементов на странице
def get_page_text(page_number):
    start_idx = (page_number - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_items = items[start_idx:end_idx]
    return "\n".join(page_items)


# Команда /start - начинаем с первой страницы
@bot.message_handler(commands=['start'])
def start_message(message):
    current_page = 1
    total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page_text = get_page_text(current_page)
    bot.send_message(message.chat.id, page_text, reply_markup=get_pagination_keyboard(current_page, total_pages))


# Обработка нажатий на кнопки пагинации
@bot.callback_query_handler(func=lambda call: call.data.startswith("page_"))
def callback_query(call):
    current_page = int(call.data.split("_")[1])
    total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page_text = get_page_text(current_page)

    # Редактируем сообщение, заменяя текст на содержимое новой страницы
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=page_text,
                          reply_markup=get_pagination_keyboard(current_page, total_pages))


# Запуск бота
bot.polling(none_stop=True)
