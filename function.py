from g4f import Provider, ChatCompletion, models
from config import genai_api, meta_api
import google.generativeai as genai
import openai
from database import SQLiteDB


# Инициализация переводчика
user_choise = {}

db = SQLiteDB('userbot.db')


genai.configure(api_key=genai_api)
model = genai.GenerativeModel("gemini-1.5-flash")

client_openai = openai.OpenAI(
    api_key=meta_api,
    base_url="https://api.sambanova.ai/v1",
)


def g4f_response(text) -> str:
    gpt_reply = ChatCompletion.create(
        model='gpt-35-turbo',
        provider=Provider.TeachAnything,
        messages=[{"role": "user", "content": text}]
    )
    print(gpt_reply)
    return gpt_reply


def meta_response(text) -> str:
    response = client_openai.chat.completions.create(
        model='Meta-Llama-3.1-8B-Instruct',
        messages=[{"role": "user", "content": text}],
        temperature=0.1,
        top_p=0.1
    )
    
    meta_reply = response.choices[0].message.content
    print(meta_reply)
    return meta_reply


def gemini_response(text):
    response = model.generate_content(text)
    return response.text


def with_reply(func):
    async def wrapped(client, message):
        if not message.reply_to_message:
            await message.edit("<b>Reply to message is required</b>")
        else:
            return await func(client, message)

    return wrapped
