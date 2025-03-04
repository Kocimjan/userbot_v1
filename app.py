from pyrogram import Client, filters
from function import with_reply, gemini_response
import logging
import configparser
from ipaddress import ip_address
import re


# === Чтение параметров подключения из файла config.ini ===
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('pyrogram', 'API_ID')
API_HASH = config.get('pyrogram', 'API_HASH')
SESSION_NAME = config.get('pyrogram', 'SESSION_NAME')
SYSTEM_PROMPT = config.get('g4f', 'SYSTEM_PROMPT')


DOWNLOAD_PATH = "downloads"
PATTERN = re.compile(r"Устройство: (.+?);.*?IP: (\d+\.\d+\.\d+\.\d+);")

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

allowed_user_ids = [906893530, 1008114300, 5547028370, 6690844057, -1002170215858]

# пользовательский фильтр
@filters.create
def user_filter(_, __, message):
    return message.chat.id in allowed_user_ids


def get_store_by_ip(ip: str) -> str:
    subnet_mapping = {
        88: "Амид 1",
        2:  "Амид 2",
        70: "Амид 3",
        80: "Амид 4",
        50: "Амид 5",
        30: "Амид 6",
        40: "Амид 7",
        33: "Амид 8",
        9:  "Амид 9",
    }
    
    try:
        ip_obj = ip_address(ip)
        octets = str(ip_obj).split(".")
        subnet = int(octets[2])
        return subnet_mapping.get(subnet, "Неизвестная сеть")
    except ValueError:
        return "Некорректный IP-адрес"


@app.on_message(filters.command("uid", prefixes=".") & filters.me)
@with_reply
async def uid_handler(_, message):
    await message.reply_text(f'User ID: {message.reply_to_message.from_user.id}')


@app.on_message(filters.command("id", prefixes=".") & user_filter)
async def id_handler(_, message):
    await message.reply_text(f'Chat ID: {message.chat.id}')
    

@app.on_message(filters.command("гпт", prefixes="."))
async def gpt_handler(_, message):
    req_text = message.text.split(".гпт ", maxsplit=1)[1]
    if len(message.text.split(' ')) <= 1:
        return await message.reply_text('Укажите запрос', quote=True)
    msg = await message.reply('Генерация...')
    await message.reply(gemini_response(req_text), quote=True)
    await app.delete_messages(msg.chat.id, msg.id)


@app.on_message(filters.private & ~filters.me)
async def message_handler(_, message):
    try:
        username = message.from_user.username if message.from_user.username else 'Неизвестный пользователь'
        message_text = message.text if message.text else '[Нет текста]'
        print(f'Новое сообщение от {username}: {message_text}')
        text = message.text.lower()
        
        with open('userbot_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{username}: {message_text} datetime:{message.date}\n')

        if message.text.startswith('/start'):
            await message.reply_text('👋 Привет! Тута')
       
        else:
            if 'привет' in text:
                await message.reply_text('Привет! Как дела? 😊')

    except Exception as e:
        print(f'❌ Произошла ошибка: {e}')


@app.on_message(filters.text & user_filter) 
async def extract_device_ip(_, message):
    match = PATTERN.search(message.text)
    if match:
        device_name = match.group(1)  
        ip_address = match.group(2) 
        
        print(f"Название устройства: {device_name}, IP-адрес: {ip_address}")
        await message.reply(get_store_by_ip(ip_address))



print('starting')
# Запуск обработки сообщений
app.run()
