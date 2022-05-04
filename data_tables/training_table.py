import sqlalchemy
from data.db_session import SqlAlchemyBase  # импорт sqlalchemy

'''Создание таблицы с тренировками'''


class Training(SqlAlchemyBase):
    __tablename__ = 'trainings'  # название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # само упражнение

    def __repr__(self):
        return "<Training('%s','%s')>" % (self.id, self.text)  # нормальный вывод
