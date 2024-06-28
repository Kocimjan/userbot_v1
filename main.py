from pyrogram import Client, filters 
from gtts import gTTS 
# from db import Database
import tgcrypto, logging, time

api_id = 24073458
api_hash = "717a1a4a14165bd46f9e066ee639a63f"

app = Client("my_app", api_id=api_id, api_hash=api_hash)
chat_id = [906893530]
muts = []

logging.basicConfig(level=logging.INFO)


# @app.on_message(filters.command("мут", prefixes=""))
# async def mute(client, message):
#   if message.chat.id != chat_id:
#     return
#   repl = message.reply_to_message
#   if repl is None:
#     return await message.reply_text("Кого?")
    
#   member = await app.get_chat_member(chat_id=message.chat.id, user_id=repl.from_user.id)
#   if member.status == member.status.OWNER or member.status == member.status.ADMINISTRATOR:
#     return await message.reply_text("он админ. его нельзя замутить")
  
#   member = await app.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
#   if member.status != member.status.OWNER and member.status != member.status.ADMINISTRATOR:
   
#     return await message.reply_text("ты не админ")
   
#   if repl.from_user.id in muts:
#     return await message.reply_text("он и так в муте")
   
#   muts.append(repl.from_user.id)
#   await message.reply_text(f"Чел {repl.from_user.first_name} замучен")


# @app.on_message(filters.command("размут", prefixes=""))
# async def mute(client, message):
#   if message.chat.id != chat_id:
#     return
#   repl = message.reply_to_message
#   if repl is None:
#     return await message.reply_text("Кого?")
  
#   member = await app.get_chat_member(chat_id=message.chat.id, user_id=repl.from_user.id)
#   if member.status == member.status.OWNER or member.status == member.status.ADMINISTRATOR:
#     return
  
#   member = await app.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
#   if member.status != member.status.OWNER and member.status != member.status.ADMINISTRATOR:
#     return
  
#   if repl.from_user.id not in muts:
#     return await message.reply_text("он не замучен")
   
#   muts.remove(repl.from_user.id)
#   await message.reply_text(f"Чел {repl.from_user.first_name} размучен")



  
# last_mes = {}
  
  
@app.on_message(lambda _, message: message.chat.id == chat_id)
async def shalash_chat(client, message):
  user_id = message.from_user.id 
  name = f"{message.from_user.first_name}"
  username = message.from_user.username 
  # await db.new_user(user_id, name, username)
#   if user_id not in last_mes:
#     last_mes[user_id] = 0
  
#   if time.time() - last_mes[user_id] <= 0.6:
#     last_mes[user_id] = time.time()
#     return await message.delete()
#   last_mes[user_id] = time.time()
  
#   if message.from_user.id in muts:
#     return await message.delete()
    
#   await db.plus_mes(user_id)
  text = message.text.lower() 
#   count = 20
#   if text.split()[0] in ["топ", "стата"]:
#     try: count = int(text.split()[1])
#     except IndexError: pass
#     except: await message.reply_text("цифрой укажи  до скольки топ")
#     if count not in range(1, 101):
#       return await message.reply_text("Предел топа сообщений: 1-100")
    
#     top = await db.get_top_messages(count)
    
#     text_top = f"Топ {count if count else 20} общительных пользователей:\n\n"
#     c = 0
#     for name, username, msgs in top:
#       c += 1
#       user = f"<a href='https://t.me/{username}'>{name}</a>"
#       text_top += f"{c}. {user} - {msgs}\n"
    
#     await message.reply_text(text_top, disable_web_page_preview=True)
    
#   if text == "/start":
#     return await message.reply_text("На месте👺")
    
#   elif text in ["/rules", "правила", "правила чата"]:
#     return await message.reply_text("""💬Комментарии для @eleday👈

# 💬Правила:

# - без 🗑политики и 🕋религии
# - без ❌мата (по возможности)

# - ✍без оскорблений

# - 💬без спама

# - 👦без контента "для 🍡взрослых"

# 💬- если нужен 🖐определённый человек, можно отметить его ✏️с помощью @

# 💬По всем вопросам: @eleday_me""")

 
  if text == "бот":
    return await message.reply_text("Сам бот. ")
  
  
app.run()