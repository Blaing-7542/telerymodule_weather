from pyrogram import Client, filters
import requests
from datetime import datetime, timedelta

with open("userbot.info", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip()

cinfo = f"☀`{prefix_userbot}weather`"
ccomand = " показывает погоду в любом городе. Пример: `weather Москва`"

# Для API нужен API_KEY. Взять его можно на сайте "https://home.openweathermap.org"
with open("owmapi.info", "r") as file:
    lines = file.readlines()
    API_KEY = lines[0].strip()


def command_weather(app):
    @app.on_message(filters.command("weather", prefixes=prefix_userbot))
    def weather(_, message):
        town = message.text.split(" ", maxsplit=1)[1]
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={town}&appid={API_KEY}&units=metric&lang=ru")
        data = response.json()
        if response.status_code == 200:
            town = data['name']
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            timezone_offset = data['timezone']
            weather_rus, emoji = weather_translation.get(weather_description, (weather_description, "❓"))
            if emoji == "❓":
                weather_rus = weather_description
            time_weather = (datetime.utcnow() + timedelta(seconds=timezone_offset)).strftime('%H:%M')
            reply_text = (f"**🏙Город:** {town}\n"
                          f"**🌡Температура:** {temperature}°C\n"
                          f"**{emoji}Погода:** {weather_rus}\n"
                          f"**⌛Время: {time_weather}**")
        else:
            reply_text = "**❌Произошла ошибка при получении данных о погоде.**"
        message.reply_text(reply_text)

weather_translation = {
    "ясно": ("ясное небо", "☀️"),
    "небольшая облачность": ("малооблачно", "🌤"),
    "облачно с прояснениями": ("облачно с прояснениями", "⛅"),
    "пасмурно": ("пасмурно", "☁️"),
    "небольшой дождь": ("небольшой дождь", "🌧"),
    "дождь": ("дождь", "🌧"),
    "гроза": ("гроза", "⛈"),
    "снег": ("снег", "❄️"),
    "туман": ("туман", "🌫"),
    "переменная облачность": ("переменная облачность", "🌤"),
}

print("Модуль weather загружен!")
