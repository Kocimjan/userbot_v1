import requests
# from create_bot import bot
# from os import getenv
import datetime
import telebot
# import os

API_KEY = ("")
bot = telebot.TeleBot(API_KEY)

WEATHER_API_KEY = ("7e3d9152a07b807c5986942d9d505e2c")

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={WEATHER_API_KEY}&lang=ru"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != "200":
        return None
    return data

def format_weather(data, day):
    city = data["city"]["name"]
    now = data["list"][0]
    current_weather = (
        f"{city}\n"
        f"Сейчас: {now['main']['temp']}°C, ощущается как {now['main']['feels_like']}°C, "
        f"ветер {now['wind']['speed']} м/c, давление {now['main']['pressure']} мм рт. ст., "
        f"влажность {now['main']['humidity']}%, {now['weather'][0]['description']}"
    )

    forecast = {}
    for entry in data["list"]:
        date_time = entry["dt_txt"]
        date = date_time.split(" ")[0]
        time = date_time.split(" ")[1]
        if date not in forecast:
            forecast[date] = []
        forecast[date].append(f"{time[:5]}: {entry['main']['temp']}°C, {entry['weather'][0]['description']}")

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    if day == "today":
        weather_report = f"{current_weather}\n\nСегодня:\n" + "\n".join(forecast.get(today, []))
    elif day == "tomorrow":
        weather_report = f"{current_weather}\n\nЗавтра:\n" + "\n".join(forecast.get(tomorrow, []))
    else:
        weather_report = (
            f"{current_weather}\n\nСегодня:\n" + "\n".join(forecast.get(today, [])) +
            "\n\nЗавтра:\n" + "\n".join(forecast.get(tomorrow, []))
        )
    return weather_report

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    if "погода на сегодня" in text:
        city = text.split("погода на сегодня")[-1].strip() or "Moscow"
        data = get_weather_data(city)
        if data:
            weather_report = format_weather(data, "today")
            bot.reply_to(message, weather_report)
        else:
            bot.reply_to(message, "Город не найден.")
    elif "погода на завтра" in text:
        city = text.split("погода на завтра")[-1].strip() or "Moscow"
        data = get_weather_data(city)
        if data:
            weather_report = format_weather(data, "tomorrow")
            bot.reply_to(message, weather_report)
        else:
            bot.reply_to(message, "Город не найден.")
    elif "погода" in text:
        city = text.split("погода")[-1].strip() or "Moscow"
        data = get_weather_data(city)
        if data:
            weather_report = format_weather(data, "all")
            bot.reply_to(message, weather_report)
        else:
            bot.reply_to(message, "Город не найден.")

if __name__ =='__main__':
    print('starting')
    bot.polling(none_stop=True, interval=0)
    
    
