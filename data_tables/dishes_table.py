import sqlalchemy
from data.db_session import SqlAlchemyBase  # импорт sqlalchemy

'''Создание таблицы с блюдами'''


class Dish(SqlAlchemyBase):
    __tablename__ = 'dishes'  # название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id блюда
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # название блюда
    dish_photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)  # фото блюда
    photo_recipe = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)  # фото рецепта блюда

    def __repr__(self):
        return "<Dish('%s','%s', '%s', '%s')>" % (
            self.id, self.name, self.dish_photo, self.photo_recipe)  # даем нормальный вид вывода
