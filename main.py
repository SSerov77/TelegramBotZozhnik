from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bot_fiels.food import Food
from bot_fiels.keyboard_markup import get_keyboard_food, get_keyboard_training

from data.config import TOKEN
from bot_fiels import keyboard_markup as kb
from random import choice
from bot_fiels.weather import Weather
from data import db_session
from data.db_session import global_init
from data.other_data import facts, quots, help_text, exercises, exer

from data_tables.users_table import User
from bot_fiels.send_photo import Photo

import asyncio
import aioschedule

user_data = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_data_dish = {}
menu = []

admin_user_data = []

global_init("db/database.db")
db_sess = db_session.create_session()

'''Пользователь'''


def register(chat_id, name):
    user = User()
    res = db_sess.query(User).filter(User.chat_id == chat_id).all()
    if not res:
        user.name = name
        user.chat_id = chat_id
        user.completion_notification = 'True'
        user.mailing = 'True'
        user.admin = 'False'
        db_sess.add(user)
        db_sess.commit()


def update_data():
    global admin_user_data
    data = db_sess.query(User).all()
    for i in data:
        tot = []
        id = i.chat_id
        name = i.name
        city = i.city
        mail = i.mailing
        comp = i.completion_notification
        tot = [id, name, city, mail, comp]
        admin_user_data.append(tot)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}, если возникнут вопросы напиши /help',
                           reply_markup=kb.mainMenu)
    register(message.from_user.id, message.from_user.first_name)


@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
    global menu
    await bot.send_message(message.from_user.id, help_text, reply_markup=kb.mainMenu)


@dp.message_handler(commands=['settings'])
async def command_start(message: types.Message):
    res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()
    if res.admin == 'True':
        await bot.send_message(message.from_user.id, 'Вы перешли в настройки',
                               reply_markup=kb.settingsMenuAdmin)
    else:
        await bot.send_message(message.from_user.id, 'Вы перешли в настройки',
                               reply_markup=kb.settingsMenu)


'''Переключение между клавиатурами'''


@dp.message_handler(text=['Другое'])
async def other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Другое"', reply_markup=kb.otherMenu)


@dp.message_handler(text=['Назад в "Другое"'])
async def back_to_other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в "Другое"', reply_markup=kb.otherMenu)


@dp.message_handler(text=['Назад в главное меню'])
async def nutrition_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=kb.mainMenu)


'''Правильное питание'''


@dp.message_handler(text=['Правильное питание'])
async def main_menu_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Правильное питание', reply_markup=kb.purposeMenu)


@dp.message_handler(text=['Назад в "Правильное питание"'])
async def nutrition_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернусь в "Правильное питание"',
                           reply_markup=kb.purposeMenu)


@dp.message_handler(text=['Супы', 'Салаты', 'Горячее', 'Рыба', 'Напитки'])
async def other_kb(message: types.Message):
    global menu
    menu = Food(str(message.text)).result
    user_data_dish[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, f'Блюдо: {menu[user_data_dish[message.from_user.id]]}',
                           reply_markup=get_keyboard_food())


@dp.callback_query_handler(text='up')
async def countdown(call: types.CallbackQuery):
    global menu
    user_index = user_data_dish[call.from_user.id]
    try:
        await call.message.edit_text(f'Блюдо: {menu[user_index + 1]}', reply_markup=get_keyboard_food())
        user_data_dish[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'Блюдо: {menu[0]}', reply_markup=get_keyboard_food())
        user_data_dish[call.from_user.id] = 0
    await call.answer()


@dp.callback_query_handler(text='down')
async def countdown(call: types.CallbackQuery):
    global menu
    user_index = user_data_dish[call.from_user.id]
    try:
        await call.message.edit_text(f'Блюдо: {menu[user_index - 1]}', reply_markup=get_keyboard_food())
        user_data_dish[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Блюдо: {menu[len(menu)]}', reply_markup=get_keyboard_food())
        user_data_dish[call.from_user.id] = len(menu)
    await call.answer()


@dp.callback_query_handler(text='finish')
async def callbacks_confirm(call: types.CallbackQuery):
    global menu
    user_index = user_data_dish[call.from_user.id]
    result = Photo(menu[user_index]).photo
    result2 = Photo(menu[user_index]).photo2
    await call.message.answer_photo(photo=result)
    await call.message.answer_photo(photo=result2)
    await call.answer()


'''Тренировки'''


@dp.message_handler(text='Тренировки')
async def workout(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Вы перешли в раздел "Тренировки", введите команду или выберите из предложенных',
                           reply_markup=kb.exerciseMenu)


@dp.message_handler(text='Случайное упражнение')
async def random_exercise(message: types.Message):
    exercise = choice(exercises)
    data = exer
    await bot.send_message(message.from_user.id, f'Упражнение: {exercise}\n{data[exercises.index(exercise)]}')


@dp.message_handler(text='Выбрать упражнение')
async def choice_exercise(message: types.Message):
    user_data[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, f'Упражнение: {exercises[user_data[message.from_user.id]]}',
                           reply_markup=get_keyboard_training())


@dp.callback_query_handler(text='back')
async def back(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Упражнение: {exercises[user_index - 1]}', reply_markup=get_keyboard_training())
        user_data[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Упражнение: {exercises[11]}', reply_markup=get_keyboard_training())
        user_data[call.from_user.id] = 11
    await call.answer()


@dp.callback_query_handler(text='next')
async def callbacks_next(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Упражнение: {exercises[user_index + 1]}', reply_markup=get_keyboard_training())
        user_data[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'Упражнение: {exercises[0]}', reply_markup=get_keyboard_training())
        user_data[call.from_user.id] = 0
    await call.answer()


@dp.callback_query_handler(text='confirm')
async def confirm(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    data = exer
    await call.message.edit_text(f'Упражнение: {exercises[user_index]}\n{data[user_index]}')
    await call.answer()


'''Погода'''


@dp.message_handler(text=['Погода'])
async def weather_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Погода"', reply_markup=kb.weatherMenu)


@dp.message_handler(text=['Узнать погоду'])
async def weather_kb(message: types.Message):
    res = Weather(str(message.chat.id)).result
    if res:
        await bot.send_message(message.from_user.id, res, reply_markup=kb.weatherMenu)
    else:
        await bot.send_message(message.from_user.id, f'Вы не ввели город', reply_markup=kb.weatherMenu)


@dp.message_handler(text=['Поменять город'])
async def weather_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
                           reply_markup=kb.weatherMenu)


@dp.message_handler(commands=['choicecity'])
async def command_start(message: types.Message):
    try:
        new_city = message.get_args()
        res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()
        res.city = new_city
        db_sess.commit()
    except:
        await bot.send_message(message.from_user.id, 'Некоректный запрос')
    else:
        await bot.send_message(message.from_user.id, f'Ваш город был изменён на: {new_city}')


'''Мотивация и Факты'''


@dp.message_handler(text='Мотивация')
async def quotes(message: types.Message):
    await bot.send_message(message.from_user.id, str(choice(quots)), reply_markup=kb.otherMenu)


@dp.message_handler(text='Интересные факты')
async def quotes(message: types.Message):
    await bot.send_message(message.from_user.id, str(choice(facts)), reply_markup=kb.otherMenu)


'''Уведомления пользователей'''


@dp.message_handler(text=['Уведомления'])
async def back_to_other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Уведомления"', reply_markup=kb.notifyMenu)


@dp.message_handler(text='Уведомление остановки бота')
async def notification_completion(message: types.Message):
    btn = types.InlineKeyboardButton(text="Включить", callback_data="notification_completion_on")
    btn1 = types.InlineKeyboardButton(text="Выключить", callback_data="notification_completion_off")
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(btn, btn1)
    await bot.send_message(message.from_user.id, f'Уведомление остановки бота', reply_markup=keyboard)


@dp.message_handler(text='Уведомления погоды')
async def notification_weather(message: types.Message):
    btn = types.InlineKeyboardButton(text="Включить", callback_data="notification_weather_on")
    btn1 = types.InlineKeyboardButton(text="Выключить", callback_data="notification_weather_off")
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(btn, btn1)
    await bot.send_message(message.from_user.id, f'Уведомления погоды', reply_markup=keyboard)


@dp.message_handler(text='Уведомления пользователей')
async def notification_weather(message: types.Message):
    res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()
    if res.admin == 'True':
        update_data()
        user_data[message.from_user.id] = 0
        await bot.send_message(message.from_user.id, f'Выберите пользователя:', reply_markup=kb.editingUsers)
    else:
        await bot.send_message(message.from_user.id, 'У вас нет прав администратора!')


@dp.callback_query_handler(text='notification_completion_on')
async def notification_completion_on(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о завершении работы бота были включены')
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()
    res.completion_notification = 'True'
    db_sess.commit()


@dp.callback_query_handler(text='notification_completion_off')
async def notification_completion_off(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о завершении работы бота были выключены')
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()
    res.completion_notification = 'False'
    db_sess.commit()


@dp.callback_query_handler(text='notification_weather_on')
async def notification_weather_on(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о погоде были включены')
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()
    res.mailing = 'True'
    db_sess.commit()


@dp.callback_query_handler(text='notification_weather_off')
async def notification_weather_off(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о погоде были выключены')
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()
    res.mailing = 'False'
    db_sess.commit()


'''Функционал Админа'''


@dp.message_handler(commands=['stop'])
async def command_start(message: types.Message):
    res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()
    if res.admin == 'True':
        btn = types.InlineKeyboardButton(text="ДА!", callback_data="stop")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(btn)
        await bot.send_message(message.from_user.id, f'Вы действительно хотите остановить бота?', reply_markup=keyboard)


@dp.callback_query_handler(text='stop')
async def stop(call: types.CallbackQuery):
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()
    if res.admin == 'True':
        await call.message.edit_text('Бот остановлен!')
        await bot.answer_callback_query(call.id,
                                        text='Бот был принудительно остановлен!'
                                             ' Данное оповещение пришло всем пользователям.',
                                        show_alert=True)
        data = db_sess.query(User).filter(User.completion_notification == 'True').all()
        for i in data:
            i = i.chat_id
            await bot.send_message(i, f'Бот был остановлен, извените за неудобства😔')
        exit(0)
    else:
        await call.message.edit_text('У вас нет прав администратора!')


@dp.callback_query_handler(text='back_choice_user')
async def back_choice_user(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    await call.message.edit_text(f'ID: {admin_user_data[user_index][0]}\n'
                                 f'Имя: {admin_user_data[user_index][1]}\n'
                                 f'Город: {admin_user_data[user_index][2]}\n'
                                 f'Уведомления о погоде: {admin_user_data[user_index][3]}\n'
                                 f'Уведомление о принудительной остановки бота: {admin_user_data[user_index][4]}',
                                 reply_markup=kb.editingUsers)
    await call.answer()


@dp.callback_query_handler(text='disabling_bot')
async def disabling_bot(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    await call.message.edit_text(f'ID: {admin_user_data[user_index][0]}\n'
                                 f'Имя: {admin_user_data[user_index][1]}\n'
                                 f'Город: {admin_user_data[user_index][2]}\n'
                                 f'Уведомления о погоде: {admin_user_data[user_index][3]}\n'
                                 f'Уведомление о принудительной остановки бота: {admin_user_data[user_index][4]}',
                                 reply_markup=kb.on_off_disabling_bot)
    await call.answer()


@dp.callback_query_handler(text='admin')
async def admin(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    await call.message.edit_text(f'ID: {admin_user_data[user_index][0]}\n'
                                 f'Имя: {admin_user_data[user_index][1]}\n'
                                 f'Город: {admin_user_data[user_index][2]}\n'
                                 f'Уведомления о погоде: {admin_user_data[user_index][3]}\n'
                                 f'Уведомление о принудительной остановки бота: {admin_user_data[user_index][4]}',
                                 reply_markup=kb.on_off_admin)
    await call.answer()


@dp.callback_query_handler(text='weather')
async def weather(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    await call.message.edit_text(f'ID: {admin_user_data[user_index][0]}\n'
                                 f'Имя: {admin_user_data[user_index][1]}\n'
                                 f'Город: {admin_user_data[user_index][2]}\n'
                                 f'Уведомления о погоде: {admin_user_data[user_index][3]}\n'
                                 f'Уведомление о принудительной остановки бота: {admin_user_data[user_index][4]}',
                                 reply_markup=kb.on_off_weather)
    await call.answer()


@dp.callback_query_handler(text='back_user')
async def back_user(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'ID: {admin_user_data[user_index - 1][0]}\n'
                                     f'Имя: {admin_user_data[user_index - 1][1]}\n'
                                     f'Город: {admin_user_data[user_index - 1][2]}\n'
                                     f'Уведомления о погоде: {admin_user_data[user_index - 1][3]}\n'
                                     f'Уведомление о принудительной остановки бота: {admin_user_data[user_index - 1][4]}',
                                     reply_markup=kb.editingUsers)
        user_data[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'ID: {admin_user_data[-1][0]}\n'
                                     f'Имя: {admin_user_data[-1][1]}\n'
                                     f'Город: {admin_user_data[-1][2]}\n'
                                     f'Уведомления о погоде: {admin_user_data[-1][3]}\n'
                                     f'Уведомление о принудительной остановки бота: {admin_user_data[-1][4]}'
                                     f'', reply_markup=kb.editingUsers)
        user_data[call.from_user.id] = -1
    await call.answer()


@dp.callback_query_handler(text='next_user')
async def next_user(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'ID: {admin_user_data[user_index + 1][0]}\n'
                                     f'Имя: {admin_user_data[user_index + 1][1]}\n'
                                     f'Город: {admin_user_data[user_index + 1][2]}\n'
                                     f'Уведомления о погоде: {admin_user_data[user_index + 1][3]}\n'
                                     f'Уведомление о принудительной остановки бота: {admin_user_data[user_index + 1][4]}',
                                     reply_markup=kb.editingUsers)
        user_data[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'ID: {admin_user_data[0][0]}\n'
                                     f'Имя: {admin_user_data[0][1]}\n'
                                     f'Город: {admin_user_data[0][2]}\n'
                                     f'Уведомления о погоде: {admin_user_data[0][3]}\n'
                                     f'Уведомление о принудительной остановки бота: {admin_user_data[0][4]}',
                                     reply_markup=kb.editingUsers)
        user_data[call.from_user.id] = 0
    await call.answer()


@dp.callback_query_handler(text='confirm_user')
async def confirm_user(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    await call.message.edit_text(f'ID: {admin_user_data[user_index][0]}\n'
                                 f'Имя: {admin_user_data[user_index][1]}\n'
                                 f'Город: {admin_user_data[user_index][2]}\n'
                                 f'Уведомления о погоде: {admin_user_data[user_index][3]}\n'
                                 f'Уведомление о принудительной остановки бота: {admin_user_data[user_index][4]}',
                                 reply_markup=kb.choiceEdit)
    await call.answer()


# ф-ция реализованна в ветке master
@dp.callback_query_handler(text='on_off_disabling_bot')
async def on_off_disabling_bot(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    id = admin_user_data[user_index][0]
    res = db_sess.query(User).filter(User.chat_id == id).first()
    if res.completion_notification == 'True':
        res.completion_notification = 'False'
    else:
        res.completion_notification = 'True'
    db_sess.commit()


@dp.callback_query_handler(text='on_off_weather')
async def on_off_weather(call: types.CallbackQuery):
    pass


@dp.callback_query_handler(text='on_off_admin')
async def on_off_admin(call: types.CallbackQuery):
    pass


@dp.message_handler()
async def echo_message(msg: types.Message):
    pass


'''Погода каждое утро'''


@dp.message_handler()
async def morning_weather():
    try:
        data = db_sess.query(User).filter(User.mailing == 'True').all()
        for i in data:
            i = i.chat_id
            # Погода реализованна в ветке master
            await bot.send_message(*i, text="Здесь должна быть погода")
    except TypeError:
        pass


async def scheduler():
    try:
        aioschedule.every().day.at("8:00").do(morning_weather)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(60)
    except TypeError:
        pass


async def on_startup(dp):
    asyncio.create_task(scheduler())


# @dp.message_handler(text='Начать тренировку')
# async def workout_start(message: types.Message):
#     btn = types.InlineKeyboardButton(text="ДА!", callback_data="yes")
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(btn)
#     await bot.send_message(message.from_user.id, f'Начинаем?', reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text='yes')
# async def yes(call: types.CallbackQuery):
#     for i in range(5, 0, -1):
#         await call.message.edit_text(str(i))
#         sleep(1)
#     data = exer
#     for i in exercises:
#         await call.message.edit_text(f'Упражнение: {i}\n{data[exercises.index(i)]}')
#         sleep(30)
#     await call.answer()

# @dp.message_handler(text=['Поменять город'])
# async def weather_kb(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
#                            reply_markup=kb.weatherMenu)

# @dp.message_handler(commands=['start'])
# async def command_start(message: types.Message):
#     if not cur.execute(f'''select chat_id From users
#                         where chat_id = '{message.chat.id}' ''').fetchall():
#         cur.execute("INSERT INTO users(chat_id, name, weight, city, mailing, completion_notification)"
#                     "VALUES(?, ?, ?, ?, ?, ?)",
#                     (message.chat.id, str(message.from_user.first_name), None, None, 'False', 'True'))
#         connection.commit()

# @dp.message_handler(text='Тренировки')
# async def workout(message: types.Message):
#     await bot.send_message(message.from_user.id,
#                            'Вы перешли в раздел "Тренировки", введите команду или выберите из предложенных',
#                            reply_markup=kb.exerciseMenu)


# @dp.callback_query_handler(text='yes')
# async def yes(call: types.CallbackQuery):
#     for i in range(5, 0, -1):
#         await call.message.edit_text(str(i))
#         sleep(1)
#     data = exer
#     for i in exercises:
#         await call.message.edit_text(f'Упражнение: {i}\n{data[exercises.index(i)]}')
#         sleep(30)
#     await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
