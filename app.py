from pyrogram import Client, filters
from config import tg_api_id, tg_api_hash
from function import with_reply, user_choise, meta_response, g4f_response, gemini_response
import requests
import io

# Инициализация клиента
app = Client("myboter", api_id=tg_api_id, api_hash=tg_api_hash)

# Список user_id, которые нужно фильтровать
allowed_user_ids = [906893530, 1008114300, 5547028370, 6690844057]  # Замените на свои chat.id


# Создаем пользовательский фильтр
@filters.create
def chat_filter(_, __, message):
    return message.from_user.id in allowed_user_ids


@app.on_message(filters.command("гпт", prefixes="."))
async def gpt_handler(_, message):
    user_id = message.from_user.id
    us = user_choise[user_id] = 'meta'
    req_text = message.text.split(".гпт ", maxsplit=1)[1]
    if len(message.text.split(' ')) <= 1:
        return await message.reply_text('Укажите запрос', quote=True)
    msg = await message.reply('Генерация...')
    if us == 'meta': 
        await message.reply(meta_response(message.text))
    elif us == 'gemini': 
        await message.reply(gemini_response(message.text))
    elif us == 'g4f':
        await message.reply(g4f_response(message.text))
    # await message.reply(g4f_response(req_text), quote=True)
    await app.delete_messages(msg.chat.id, msg.id)


@app.on_message(filters.command(["q", "quote"], prefixes='.') & filters.me)
@with_reply
async def handle_sq_command(client, message):
    reply = message.reply_to_message

    if not reply:
        await message.reply("❗️ Пожалуйста, ответьте на сообщение.")
        return

    # Извлекаем текст из ответного сообщения
    message_text = reply.text or "Нет текста для цитаты"
    print(message_text)
    # Подготовка данных для API запроса
    api_url = "https://quotes.fl1yd.su/generate"
    payload = {
        "messages": [
            {
                "text": message_text,
                "author": {
                    "id": reply.from_user.id,  # Добавляем поле id автора
                    "name": reply.from_user.first_name,
                },
                # Поле reply как словарь с минимальной информацией
                "reply": {
                    "id": message.id,
                    "text": message.text or "Нет текста в ответе"
                }
            }
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

    # Отправка запроса на API для генерации цитаты
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        quote_image = io.BytesIO(response.content)
        quote_image.name = "quote.webp"
        await message.reply_document(document=quote_image)
    else:
        await message.reply("❗️ Ошибка при создании цитаты.")


print('starting')
# Запуск обработки сообщений
app.run()
