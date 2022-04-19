import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Dish(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)

    # def __repr__(self):
    #     return

