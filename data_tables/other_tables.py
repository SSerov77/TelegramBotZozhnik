import sqlalchemy
from data.db_session import SqlAlchemyBase  # импорт sqlalchemy

'''Создание таблицы с фактами'''


class Fact(SqlAlchemyBase):
    __tablename__ = 'facts'  # название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id факта
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # сам факт

    def __repr__(self):
        return "<Fact('%s','%s')>" % (self.id, self.text)  # нормальный вывод


'''Создание таблицы с мотивацией'''


class Quot(SqlAlchemyBase):
    __tablename__ = 'quotes'  # название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id цитаты
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # сама цитата

    def __repr__(self):
        return "<Quot('%s','%s')>" % (self.id, self.text)  # нормальный вывод
