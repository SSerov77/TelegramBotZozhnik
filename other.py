from data import db_session
from data.db_session import global_init
from data.other_tables import Quot

global_init("db/database.db")
db_sess = db_session.create_session()






