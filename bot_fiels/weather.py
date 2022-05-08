import requests  # импорт reqests
from data.config import WEATHER_TOKEN  # API погоды
from data import db_session  # импорт БД
from data.db_session import global_init  # импорт создания БД
from data_tables.users_table import User  # импорт таблицы User из БД

global_init("db/database.db")  # подключение к БД
db_sess = db_session.create_session()  # создание БД

''' Класс с функцией погоды'''

slv = {'Clouds': 'Облачно', 'Rain': 'Идёт дождь', 'Clear': 'Ясно',
       'Snow': 'Идёт снег', 'Mist': 'Туман'}  # словарь общей погоды для рассылка на русском


class Weather:
    def __init__(self, chat_id):
        self.chat_id = chat_id  # получаем id пользователя
        self.result = ''
        self.weather()  # вызываем функцию weather

    def weather(self):  # функция получения погоды
        try:
            res = ''
            result = db_sess.query(User).filter(
                User.chat_id == self.chat_id).first()  # Получаем город пользователя из БД
            result = str(result.city).lstrip().rstrip()  # обрабатываем город пользлвателя
            if result == '':  # проверка реузльтата города
                self.result = 'Ваш город не найден или вы его не ввели'  # если нет города
            else:
                r = requests.get(
                    f"http://api.openweathermap.org/geo/1.0/direct?q={result}&appid={WEATHER_TOKEN}"
                    # Переводим город в координаты
                )

                first_data = r.json()  # получаем json файл
                lat = first_data[0]['lat']  # Получаем координаты
                lon = first_data[0]['lon']  # Получаем координаты
                res = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}"
                    # Получаем информацию о погоде по городу
                )

                data = res.json()  # получаем json файл
                user_city = result  # город
                main_weather = slv[data['weather'][0]['main']]  # оcновная погода
                temp = int(data['main']['temp']) - 273  # температура
                humidity = data['main']['humidity']  # влажность
                pressure = data['main']['pressure']  # давление
                result = str(f'Погода в городе {user_city}:\n'
                             f'Сегодня: {main_weather}\n'  # выводимый результат
                             f'Температура: {temp}C\n'  # температура
                             f'Влажность: {humidity}%\n'  # давление
                             f'Давление: {int(pressure) * 0.75} мм.рт.ст'  # перевод давления в мм.рт.ст
                             )
                self.result = result  # отправляем результат
        except Exception:
            if result.lower() == 'верхний пчеловодск' or result.lower() == 'верхний-пчеловодск':
                self.result = 'В Верхнем Пчеловодске живут Артёмы Олеговичи, которые ставят за проекты 100 баллов.' \
                              ' Они хотят отметить и купить тортик в честь окончания Яндекс Лицея их любимых студентов! ' \
                              'Помогают в размещении бота на сервере и его тестировании. Их любимое блюдо это лосось фаршированный' \
                              ' редисками. Ах да, о погоде, там всегда тепло и солнечно, летают пчёлы, прекрасное время, чтобы ' \
                              'к семи часам вечера поехать кататься на велосипедах 30км.)'
            else:
                self.result = f'{result} не найден, но там наверное тепло)'  # если город не найден
