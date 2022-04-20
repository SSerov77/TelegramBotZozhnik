from aiogram import Bot, types
from config import TOKEN
from data import db_session
from data.db_session import global_init
from data.dishes import Dish

bot = Bot(token=TOKEN)
global_init("db/database.db")


class Photo:
    def __init__(self, number):
        self.number = number
        self.read_blob_data()

    def read_blob_data(self):
        dish = Dish()
        db_sess = db_session.create_session()
        res = db_sess.query(Dish).filter(Dish.id == self.number).first()
        self.photo = res.photo

