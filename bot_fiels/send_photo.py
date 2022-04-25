from aiogram import Bot
from data.config import TOKEN
from data import db_session
from data.db_session import global_init
from data.dishes_table import Dish

bot = Bot(token=TOKEN)
global_init("../db/database.db")


class Photo:
    def __init__(self, name):
        self.name = name
        self.read_blob_data()

    def read_blob_data(self):
        dish = Dish()
        db_sess = db_session.create_session()
        res = db_sess.query(Dish).filter(Dish.name == self.name).first()
        self.photo = res.dish_photo
        self.photo2 = res.photo_recipe

