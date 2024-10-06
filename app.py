# main.py
from pyrogram import Client, filters
from config import tg_api_id, tg_api_hash
from function import gpt_response, get_weather, user_messages

# Инициализация клиента
app = Client("mybot", api_id=tg_api_id, api_hash=tg_api_hash)

# Список chat_id, которые нужно фильтровать
allowed_user_ids = [906893530, 1008114300, 5547028370, 6690844057]  # Замените на свои chat.id


# Создаем пользовательский фильтр
@filters.create
def chat_filter(_, __, message):
    return message.from_user.id in allowed_user_ids


@app.on_message(filters.command("погода", prefixes=".") & chat_filter)
async def weather_handler(client, message):
    if len(message.text.split(' ')) > 1:
        city = message.text.split(' ')[1]
        print(city)
        await get_weather(message, city=city)
    else:
        await message.reply_text('Не указан город', quote=True)


# Обработчик для команды "гпт"
@app.on_message(filters.command("гпт", prefixes=".") & chat_filter)
async def gpt_handler(client, message):
    if len(message.text.split(' ')) <= 1:
        return await message.reply_text('Укажите запрос', quote=True)
    else:
        print(message.from_user.id, message.text)
    if message.from_user.id not in user_messages:
        user_messages[message.from_user.id] = []
    await message.reply(gpt_response(message), quote=True)


print('sss')
app.run()  # Корректный запуск бота
