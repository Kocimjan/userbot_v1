import os


def get_env_variables():
    # Проверка и получение переменных окружения
    # tg_api_id = os.getenv('tg_api_id')
    # tg_api_hash = os.getenv('tg_api_hash')
    # weather_api_key = os.getenv('weather_api_key')

    tg_api_id = 12585237
    tg_api_hash = '6518b2191f6d03703cca46a80e7ddef8'
    weather_api_key = '7e3d9152a07b807c5986942d9d505e2c'


    # Если переменные не установлены, запрашиваем их у пользователя
    if not tg_api_id:
        tg_api_id = input("Введите значение tg_api_id: ")

    if not tg_api_hash:
        tg_api_hash = input("Введите значение tg_api_hash: ")

    if not weather_api_key:
        weather_api_key = input("Введите значение weather_api_key: ")

    return tg_api_id, tg_api_hash, weather_api_key


# Пример вызова функции
tg_api_id, tg_api_hash, weather_api_key = get_env_variables()
