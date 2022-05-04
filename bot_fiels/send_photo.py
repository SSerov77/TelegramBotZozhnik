from data import db_session  # импорт создания сессии
from data.db_session import global_init  # импорт функции проверки БД
from data_tables.dishes_table import Dish  # импорт таблицы с блюдами из БД

global_init("../db/database.db")  # подключение к БД

'''Получение фото блюда из БД'''


class Photo:
    def __init__(self, name):
        self.name = name  # название блюда
        self.read_blob_data()  # вызов функции обработки фото

    def read_blob_data(self):  # функция обработки фото
        db_sess = db_session.create_session()  # создание сессии
        res = db_sess.query(Dish).filter(Dish.name == self.name).first()  # получаем блюдо  по названию из БД
        self.photo = res.dish_photo  # фото блюда
        self.photo2 = res.photo_recipe  # фото рецепта блюда
