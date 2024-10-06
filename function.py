import requests
from g4f.client import Client
from config import weather_api_key
from collections import defaultdict


client = Client()
user_messages = defaultdict(list)


async def get_weather(message, api_key=weather_api_key, city='Худжанд'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=ru'
    response_weather = requests.get(url)
    if response_weather.status_code == 200:
        weather_data = response_weather.json()
        wind_speed = weather_data['wind']['speed']
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return await message.reply_text(f'Погода в городе {city}: {description}, Температура: {temperature}°C, '
                                        f'Скорость ветра:{wind_speed}/с', quote=True)
    else:
        return await message.reply_text('Ошибка при получении данных о погоде', response_weather, quote=True)


def gpt_response2(message) -> str:
    user_messages[message.from_user.id].append(message.text)
    print(user_messages)
    chat_completion = client.chat.completions.create(model="gpt-4o",
                                                     messages=[{"role": "user",
                                                                "content": "Какая ты модель?"}],
                                                     )
    return chat_completion.choices[0].message.content or ""


def gpt_response(message, text) -> str:
    user_id = message.from_user.id
    user_messages[user_id].append({"role": "user", "content": text})
    if len(user_messages[user_id]) > 1:
        user_messages[user_id].append({"role": "assistant", "content": user_messages[user_id][-1]["content"]})
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=user_messages[user_id]
    )
    gpt_reply = chat_completion.choices[0].message.content or ''
    user_messages[user_id].append({"role": "assistant", "content": gpt_reply})
    print(user_messages)
    return gpt_reply
