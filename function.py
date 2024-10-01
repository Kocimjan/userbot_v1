import requests
import g4f
from config import weather_api_key


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


def gpt_response(message):
    user_request = message.text
    return g4f.ChatCompletion.create(
        model="gpt-4o-mini",
        provider=g4f.Provider.ChatgptFree,
        messages=[{"role": "user", "content": user_request}],
    )

