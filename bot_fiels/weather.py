import requests
import sqlite3
from config import WEATHER_TOKEN  # API погоды

connection = sqlite3.connect('BotZozhnik.db')  # подключение БД
cur = connection.cursor()

''' Класс с функцией погоды'''


slv = {'Clouds': 'Облачно', 'Rain': 'Идёт дождь', 'Clear': 'Ясно',
       'Snow': 'Идёт снег', 'Mist': 'Туман'}

class Weather:
    def __init__(self, chat_id):
        self.chat_id = chat_id  # получаем id пользователя
        self.result = 'Error'
        self.weather()

    def weather(self):
        try:
            city = cur.execute(f'''select city From users                                               
                                    where chat_id = '{self.chat_id}' ''').fetchall()  # Получаем город пользователя из БД
            r = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={WEATHER_TOKEN}"
                # Переводим город в координаты
            )

            first_data = r.json()
            lat = first_data[0]['lat']  # Получаем координаты
            lon = first_data[0]['lon']

            res = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}"
                # Получаем информацию о погоде
            )

            data = res.json()
            user_city = city[0][0]  # город
            main_weather = slv[data['weather'][0]['main']]  # оcновная погода
            temp = int(data['main']['temp']) - 273  # температура
            humidity = data['main']['humidity']  # влажность
            pressure = data['main']['pressure']  # давление
            result = str(f'Погода в городе {user_city}:\n'
                         f'Сегодня: {main_weather}\n'  # выводимый результат
                         f'Температура: {temp}C\n'
                         f'Влажность: {humidity}%\n'
                         f'Давление: {int(pressure) * 0.75} мм.рт.ст'
                         )
            self.result = result
        except Exception:
            if city:
                self.result = f'Ваш город "{city[0][0]}" не найден, но там наверное тепло)'
