from telebot import TeleBot
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from envparse import Env

env = Env()

bot = TeleBot(token=env.str("TOKEN"))

# Инициализация бота с использованием токена
ADMIN_CHAT_ID = '362857450'  # Замените на ID чата администратора
COURIER_CHAT_ID = '362857450'  # Замените на ID чата курьера

# Пример данных о товарах
products = [
    {"name": "Товар 1", "price": "100 руб.", "callback_data": "product_1"},
    {"name": "Товар 2", "price": "200 руб.", "callback_data": "product_2"},
    {"name": "Товар 3", "price": "300 руб.", "callback_data": "product_3"}
]

# Словарь для хранения состояния пользователя (выбранные товары и личные данные)
user_states = {}

# Путь к файлу Excel
excel_file = 'orders.xlsx'


# Функция для инициализации таблицы Excel
def initialize_excel():
    try:
        pd.read_excel(excel_file)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=["Идентификатор заказа", "Имя клиента", "Номер телефона", "Адрес доставки", "Товар", "Цена",
                     "Заказ подтвержден"])
        df.to_excel(excel_file, index=False)


# Инициализация Excel таблицы
initialize_excel()


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("Привет! Это магазин в Телеграме. "
                    "Для того, чтобы просмотреть каталог товаров и сделать заказ нажми команду /shop_list. "
                    "Желаем приятных покупок!")
    bot.send_message(message.chat.id, welcome_text)


# Обработчик команды /shop_list
@bot.message_handler(commands=['shop_list'])
def send_shop_list(message):
    markup = InlineKeyboardMarkup()
    for product in products:
        button = InlineKeyboardButton(
            f"{product['name']} - {product['price']}",
            callback_data=product["callback_data"]  # Данные, которые будут прокинуты в обработчик при нажатии на кнопку
        )
        markup.add(button)
    bot.send_message(message.chat.id, "Каталог товаров:", reply_markup=markup)


# Обработчик нажатий на кнопки товаров
@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def handle_product_selection(call):
    selected_product = next((p for p in products if p["callback_data"] == call.data), None)
    if selected_product:
        user_id = call.from_user.id
        user_states[user_id] = {"product": selected_product}
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Вы выбрали {selected_product['name']} за {selected_product['price']}"
                                   f"\nКак к вам обращаться?")
        bot.register_next_step_handler(call.message, get_name)


def get_name(message):
    user_id = message.from_user.id
    if user_id in user_states:
        user_states[user_id]["name"] = message.text
        bot.send_message(message.chat.id, "Введите ваш номер телефона:")
        bot.register_next_step_handler(message, get_phone)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова.")


def get_phone(message):
    user_id = message.from_user.id
    if user_id in user_states:
        user_states[user_id]["phone"] = message.text
        bot.send_message(message.chat.id, "Введите ваш адрес доставки:")
        bot.register_next_step_handler(message, get_address)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова.")


def get_address(message):
    user_id = message.from_user.id
    if user_id in user_states:
        user_states[user_id]["address"] = message.text
        selected_product = user_states[user_id]["product"]
        name = user_states[user_id]["name"]
        phone = user_states[user_id]["phone"]
        address = user_states[user_id]["address"]

        # Генерация идентификатора заказа
        order_id = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')

        # Запись данных в Excel
        df = pd.read_excel(excel_file)
        new_order = pd.DataFrame([{
            "Идентификатор заказа": order_id,
            "Имя клиента": name,
            "Номер телефона": phone,
            "Адрес доставки": address,
            "Товар": selected_product['name'],
            "Цена": selected_product['price'],
            "Заказ подтвержден": "нет"
        }])
        df = pd.concat([df, new_order], ignore_index=True)
        df.to_excel(excel_file, index=False)

        # Отправка подтверждения пользователю
        bot.send_message(message.chat.id, f"Ваш заказ: {selected_product['name']} за {selected_product['price']}.\n"
                                          f"Имя: {name}\nТелефон: {phone}\nАдрес доставки: {address}\n"
                                          f"Идентификатор заказа: {order_id}\n"
                                          "Спасибо за заказ! В ближайшее время с вами свяжутся для подтверждения.")

        # Уведомление администратора
        markup = InlineKeyboardMarkup()
        confirm_button = InlineKeyboardButton("Подтвердить", callback_data=f"confirm_{order_id}")
        cancel_button = InlineKeyboardButton("Отменить", callback_data=f"cancel_{order_id}")
        markup.add(confirm_button, cancel_button)

        bot.send_message(ADMIN_CHAT_ID, f"НОВЫЙ ЗАКАЗ\n"
                                        f"Идентификатор заказа: {order_id}\n"
                                        f"Имя клиента: {name}\n"
                                        f"Номер телефона: {phone}\n"
                                        f"Адрес доставки: {address}\n"
                                        f"Товар: {selected_product['name']} за {selected_product['price']}",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова.")


# Обработчик нажатий на кнопки администратора
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_") or call.data.startswith("cancel_"))
def handle_admin_action(call):
    action, order_id = call.data.split("_")
    df = pd.read_excel(excel_file)
    order_index = df[df["Идентификатор заказа"].astype(str) == order_id].index

    if not order_index.empty:
        if action == "confirm":
            df.at[order_index[0], "Заказ подтвержден"] = "да"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Заказ {order_id} подтвержден.")
            send_order_to_courier(order_id, df.loc[order_index[0]])
        elif action == "cancel":
            df.at[order_index[0], "Заказ подтвержден"] = "отменен"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Заказ {order_id} отменен.")
        df.to_excel(excel_file, index=False)
    else:
        bot.send_message(call.message.chat.id, f"Заказ с идентификатором {order_id} не найден. Попробуйте снова.")


# Функция для отправки заказа курьеру
def send_order_to_courier(order_id, order_details):
    bot.send_message(COURIER_CHAT_ID, f"НОВЫЙ ЗАКАЗ ДЛЯ ДОСТАВКИ\n"
                                      f"Идентификатор заказа: {order_id}\n"
                                      f"Имя клиента: {order_details['Имя клиента']}\n"
                                      f"Номер телефона: {order_details['Номер телефона']}\n"
                                      f"Адрес доставки: {order_details['Адрес доставки']}\n"
                                      f"Товар: {order_details['Товар']}\n"
                                      f"Цена: {order_details['Цена']}\n"
                                      f"Заказ подтвержден: {order_details['Заказ подтвержден']}")


# Запуск polling
bot.polling()
