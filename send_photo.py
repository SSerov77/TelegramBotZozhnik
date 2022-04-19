import sqlite3
import os

from data import db_session
from data.db_session import global_init
from data.dishes import Dish

global_init("db/database.db")


class Photo:
    def __init__(self, number):
        self.number = number
        self.result_photo = ''
        self.read_blob_data()

    def write_to_file(self, data, filename):
        # Преобразование двоичных данных в нужный формат
        with open(filename, 'wb') as file:
            file.write(data)
        print("Данный из blob сохранены в: ", filename, "\n")

    def read_blob_data(self):
        db_sess = db_session.create_session()
        self.res = db_sess.query(Dish).filter(Dish.id == self.number).all()
        print(self.res)

        try:
            # self.write_to_file(self.res[0], photo_path)
            print('OK')
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


Photo(1)
