import sqlalchemy
from .db_session import SqlAlchemyBase


class Dish(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dish_photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    photo_recipe = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)

    def __repr__(self):
        return "<Dish('%s','%s', '%s', '%s')>" % (self.id, self.name, self.dish_photo, self.photo_recipe)
