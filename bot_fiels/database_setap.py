from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Post(DeclarativeBase):
    __tablename__ = 'info_user2'

    id = Column(Integer, primary_key=True)
    id_user = Column('id_user', String)
    name = Column('name', String)

    def __repr__(self):
        return ""


def main():
    engine = create_engine(f"sqlite:///db_bot.db")
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_post = Post(id_user=12345678, name='Сергей')

    # Добавляем запись
    session.add(new_post)
    print(new_post)

    # Благодаря этой строчке мы добавляем данные а таблицу
    session.commit()


if __name__ == "__main__":
    main()