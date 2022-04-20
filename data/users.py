import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mailing = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    completion_notification = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s')>" % (
            self.id, self.chat_id, self.name, self.city, self.mailing, self.completion_notification)
