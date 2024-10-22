import requests
import os
from time import sleep

# Замените на ваш токен бота и chat_id
API_TOKEN = os.getenv("TOKEN")
MESSAGE = 'Привет, это сообщение, отправленное через requests!'

# URL запроса
url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"


def get_user_ids_for_notifications():
    return ['362857450']


def notify_user(chat_id: str, message: str):
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    # Выполняем GET-запрос
    return requests.get(url, params=params)


while True:
    users_for_notifications = get_user_ids_for_notifications()

    for user_id in users_for_notifications:
        res = notify_user(chat_id=user_id, message=MESSAGE)
        print(res.json())
        sleep(5)
