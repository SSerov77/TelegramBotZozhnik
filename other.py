from data import db_session
from data.db_session import global_init
from data.facts import Fact

global_init("db/database.db")
db_sess = db_session.create_session()

with open('facts.txt', 'r', encoding="utf8") as f:
    data = f.readlines()
    for i in data:
        fact = Fact()
        fact.text = str(i)
        db_sess.add(fact)

db_sess.commit()



