from data import db_session
from data.db_session import global_init
from data_tables.other_tables import Fact, Quot
from data_tables.training_table import Training

global_init("db/database.db")
db_sess = db_session.create_session()

facts = []
data = db_sess.query(Fact)
for i in data:
    facts.append(i.text)

exer = []
data = db_sess.query(Training)
for i in data:
    exer.append(i.text)

quots = []
data = db_sess.query(Quot)
for i in data:
    quots.append(i.text)

help_text = 'Как пользоваться ботом?' \
            '\n❗Чтобы вызвать клавиатуру основного меню, введи команду /start' \
            '\nПосле этого выбери один из нужных тебе инструментов' \
            '\n✅Раздел "Ваше питание" подскажет тебе нужный рацион чтобы похудеть, набрать массу или поддерживать её' \
            '\n✅Раздел "Тренировки" подскажет тебе быстрые и удобные физические упражнения на каждый день' \
            '\n✅В разделе "Мои достижения" ты можешь записывать свои успехи по улучшению себя' \
            '\n✅В разделе "Уведомления" ты можешь записать что-то и бот тебе это пришлёт несколько раз ,чтобы ты не забыл об этом' \
            '\n✅В "Другое" ты найдешь еще много чего интересного:)'

exercises = ['Прыжки', 'Приседание у стены', 'Отжимания от пола', 'Подъемы на стул', 'Наклон вперед из положения лежа',
             'Приседания', 'Бег, колени вверх',
             'Выпады', 'Отжимания с поворотом', 'Боковая планка', 'Обратные отжимания от стула', 'Планка']