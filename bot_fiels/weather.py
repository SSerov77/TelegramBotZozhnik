from pprint import pprint

import requests
from config import WEATHER_TOKEN  # API погоды
from data import db_session
from data.db_session import global_init
from data.users_table import User

global_init("db/database.db")
db_sess = db_session.create_session()

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
            result = db_sess.query(User).filter(
                User.chat_id == self.chat_id).first()  # Получаем город пользователя из БД

            result = str(result.city)
            r = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={result}&appid={WEATHER_TOKEN}"
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
            user_city = result  # город
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
            if res:
                self.result = f'Ваш город "{result}" не найден, но там наверное тепло)'
