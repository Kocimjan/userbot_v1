from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
import configparser
import re
import sqlite3
from ipaddress import ip_address
# === Чтение параметров подключения из файла config.ini ===
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('pyrogram', 'API_ID')
API_HASH = config.get('pyrogram', 'API_HASH')
SESSION_NAME = config.get('pyrogram', 'SESSION_NAME')
SOURCE_CHAT_ID = int(config.get('settings', 'SOURCE_CHAT_ID'))
TARGET_CHAT_ID = int(config.get('settings', 'TARGET_CHAT_ID'))
TARGET_TOPIC_ID = int(config.get('settings', 'TARGET_TOPIC_ID'))  # ID топика, куда пересылать

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
PATTERN = re.compile(r"Устройство: (.+?);.*?IP: (\d+\.\d+\.\d+\.\d+);")

allowed_user_ids = [906893530, 1008114300, 5547028370, 6690844057]

# пользовательский фильтр
@filters.create
def chat_filter(_, __, message):
    return message.from_user.id in allowed_user_ids


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


@app.on_message(filters.text & chat_filter) 
async def extract_device_ip(_, message):
    match = PATTERN.search(message.text)
    if match:
        device_name = match.group(1)  
        ip_address = match.group(2) 
        
        print(f"Название устройства: {device_name}, IP-адрес: {ip_address}")
        await message.reply(get_store_by_ip(ip_address))

        
app.run()
