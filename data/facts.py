import sqlalchemy
from .db_session import SqlAlchemyBase


class Fact(SqlAlchemyBase):
    __tablename__ = 'facts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "<Fact('%s','%s')>" % (self.id, self.text)
