import sqlalchemy
from data.db_session import SqlAlchemyBase

'''Создание таблицы пользователей'''


class User(SqlAlchemyBase):
    __tablename__ = 'users'  # название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id
    chat_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # id юзера
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя юзера
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # город юзера
    mailing = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # уведомления
    completion_notification = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # уведомления
    admin = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # админ

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s', '%s')>" % (
            self.id, self.chat_id, self.name, self.city, self.mailing, self.completion_notification)  # нармальный вывод
