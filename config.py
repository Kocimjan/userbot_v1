import os


def get_env_variables():
    # Проверка и получение переменных окружения
    tg_api_id = os.getenv('tg_api_id')
    tg_api_hash = os.getenv('tg_api_hash')

    # Если переменные не установлены, запрашиваем их у пользователя
    if not tg_api_id:
        tg_api_id = input("Введите значение tg_api_id: ")

    if not tg_api_hash:
        tg_api_hash = input("Введите значение tg_api_hash: ")

    return tg_api_id, tg_api_hash


# Пример вызова функции
tg_api_id, tg_api_hash = get_env_variables()
AUTOREPLY_MESSAGE = "Здравствуйте! Я сейчас не могу ответить на ваше сообщение. Пожалуйста, подождите немного."
last_reply_times = {}
REPLY_INTERVAL = 3600