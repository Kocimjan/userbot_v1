from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
from config import tg_api_hash, tg_api_id, weather_api_key

app = Client("userbot", api_id=tg_api_id, api_hash=tg_api_hash)

# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)

# Команда взлома пентагона
@app.on_message(filters.command("hack", prefixes=".") & filters.me)

# Команда thanos
@app.on_message(filters.command("thanos", prefixes=".") & filters.me)
