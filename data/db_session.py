import sqlalchemy as sa  # импорт sqlachemy
import sqlalchemy.orm as orm  # импорт sqlachemy
from sqlalchemy.orm import Session  # импорт sqlachemy
import sqlalchemy.ext.declarative as dec  # импорт sqlachemy

SqlAlchemyBase = dec.declarative_base()  # импорт sqlachemy

__factory = None

'''Создание БД'''


def global_init(db_file):  # функция создания БД
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")  # если БД нет - создать

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")  # если БД найдена

    engine = sa.create_engine(conn_str, echo=False)  # создание БД
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
