from g4f import Provider, ChatCompletion, models
import google.generativeai as genai
from googletrans import Translator
import openai

# Инициализация переводчика
translator = Translator()
user_choise = {}


genai.configure(api_key='AIzaSyCUaRs9G3r-Qx7uGoV0EXFSVaolqQbkQoo')
model = genai.GenerativeModel("gemini-1.5-flash")

client_openai = openai.OpenAI(
    api_key="542312c2-dbb0-4af4-a7bf-bf007c97a61c",
    base_url="https://api.sambanova.ai/v1",
)


def translate_to_russian(text) -> str:
    # Автоматическое определение исходного языка и перевод на русский
    try:
        result = translator.translate(text, dest='ru')
        source_lang = result.src  # Определённый исходный язык
        translated_text = result.text  # Переведённый текст
        return f"Исходный язык: {source_lang}\nПеревод: {translated_text}"
    except Exception as e:
        return f"Ошибка при переводе: {e}"


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
        model='Meta-Llama-3.1-70B-Instruct',
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
