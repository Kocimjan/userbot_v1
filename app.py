from pyrogram import Client, filters
from config import tg_api_id, tg_api_hash, AUTOREPLY_MESSAGE, last_reply_times, REPLY_INTERVAL
from function import with_reply, user_choise, meta_response, g4f_response, gemini_response
import logging

# Инициализация клиента
app = Client("mybot", api_id=tg_api_id, api_hash=tg_api_hash)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Список user_id, которые нужно фильтровать
allowed_user_ids = [906893530, 1008114300, 5547028370, 6690844057]  # Замените на свои chat.id


# Создаем пользовательский фильтр
@filters.create
def chat_filter(_, __, message):
    return message.from_user.id in allowed_user_ids


@app.on_message(filters.command("гпт", prefixes="."))
async def gpt_handler(_, message):
    user_id = message.from_user.id
    req_text = message.text.split(".гпт ", maxsplit=1)[1]
    if len(message.text.split(' ')) <= 1:
        return await message.reply_text('Укажите запрос', quote=True)
    msg = await message.reply('Генерация...')
    await message.reply(g4f_response(req_text), quote=True)
    await app.delete_messages(msg.chat.id, msg.id)


# 📥 Чтение входящих сообщений без отметки "прочитано"
@app.on_message(filters.private & ~filters.me)
def message_handler(client, message):
    try:
        username = message.from_user.username if message.from_user.username else 'Неизвестный пользователь'
        message_text = message.text if message.text else '[Нет текста]'
        print(f'Новое сообщение от {username}: {message_text}')
        text = message.text.lower()

        # 📋 Сохраняем лог всех сообщений в файл
        with open('userbot_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{username}: {message_text}\n')

        # 📜 Обработка команд /start, /help и /stop
        if message.text.startswith('/start'):
            message.reply_text('👋 Привет! Тута')
       
        # 🤖 Автоответчик на обычные сообщения (если это не команда)
        else:
            # Пример логики автоответчика
            if 'привет' in text:
                message.reply_text('Привет! Как дела? 😊')
            elif 'как дела' in text:
                message.reply_text('У меня всё отлично! А у вас?')
            elif 'салом' in text:
                message.reply_text('Салом алейкум')
            elif 'дурустми' in text:
                message.reply_text('Нагз Рахмат')

    except Exception as e:
        print(f'❌ Произошла ошибка: {e}')



print('starting')
# Запуск обработки сообщений
app.run()
