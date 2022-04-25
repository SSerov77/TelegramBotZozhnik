import sqlalchemy
from data.db_session import SqlAlchemyBase


class Training(SqlAlchemyBase):
    __tablename__ = 'trainings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "<Training('%s','%s')>" % (self.id, self.text)