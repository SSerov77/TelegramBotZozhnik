import telegram as telegram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from time import sleep, time

from bot_fiels.food import Food
from bot_fiels.keyboard_markup import get_keyboard_food, get_keyboard_training

from config import TOKEN
from bot_fiels import keyboard_markup as kb
from random import choice
from bot_fiels.weather import Weather
from data import db_session
from data.db_session import global_init
from data.other_data import facts, quots, help_text, exercises

from data.users import User
from send_photo import Photo

user_data = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_data_dish = {}
menu = []

global_init("db/database.db")
db_sess = db_session.create_session()


def register(chat_id, name):
    user = User()
    res = db_sess.query(User).filter(User.chat_id == chat_id).all()
    if not res:
        user.name = name
        user.chat_id = chat_id
        user.completion_notification = 'True'
        user.mailing = 'True'
        db_sess.add(user)
        db_sess.commit()


@dp.message_handler(text=['Супы', 'Салаты', 'Горячее', 'Рыба', 'Напитки'])
async def other_kb(message: types.Message):
    global menu
    menu = Food(str(message.text)).result
    user_data_dish[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, f'Блюдо: {menu[user_data_dish[message.from_user.id]]}',
                           reply_markup=get_keyboard_food())


@dp.callback_query_handler(text='back')
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


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}, если возникнут вопросы напиши \help',
                           reply_markup=kb.mainMenu)
    register(message.from_user.id, message.from_user.first_name)


@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
    global menu
    await bot.send_message(message.from_user.id, help_text, reply_markup=kb.mainMenu)


@dp.message_handler(text=['Назад в главное меню'])
async def nutrition_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=kb.mainMenu)


@dp.message_handler(text=['Правильное питание'])
async def main_menu_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Правильное питание', reply_markup=kb.purposeMenu)


@dp.message_handler(text=['Назад в "Правильное питание"'])
async def nutrition_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернусь в "Правильное питание"',
                           reply_markup=kb.purposeMenu)


@dp.message_handler(text=['Другое'])
async def other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Другое"', reply_markup=kb.otherMenu)


@dp.message_handler(text=['Назад в "Другое"'])
async def back_to_other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в "Другое"', reply_markup=kb.otherMenu)


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


@dp.message_handler(text=['Уведомления'])
async def back_to_other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Уведомления"', reply_markup=kb.notifyMenu)


@dp.message_handler(text='Мотивация')
async def quotes(message: types.Message):
    await bot.send_message(message.from_user.id, str(choice(quots)), reply_markup=kb.otherMenu)


@dp.message_handler(text='Интересные факты')
async def quotes(message: types.Message):
    await bot.send_message(message.from_user.id, str(choice(facts)), reply_markup=kb.otherMenu)


@dp.message_handler(text=['Поменять город'])
async def weather_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
                           reply_markup=kb.weatherMenu)


@dp.message_handler(text='Уведомления погоды')
async def notification_weather(message: types.Message):
    btn = types.InlineKeyboardButton(text="Включить", callback_data="notification_weather_on")
    btn1 = types.InlineKeyboardButton(text="Выключить", callback_data="notification_weather_off")
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(btn, btn1)
    await bot.send_message(message.from_user.id, f'Уведомления погоды', reply_markup=keyboard)


@dp.message_handler(text='Уведомление остановки бота')
async def notification_completion(message: types.Message):
    btn = types.InlineKeyboardButton(text="Включить", callback_data="notification_completion_on")
    btn1 = types.InlineKeyboardButton(text="Выключить", callback_data="notification_completion_off")
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(btn, btn1)
    await bot.send_message(message.from_user.id, f'Уведомление остановки бота', reply_markup=keyboard)


@dp.message_handler(text='Тренировки')
async def workout(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Вы перешли в раздел "Тренировки", введите команду или выберите из предложенных',
                           reply_markup=kb.exerciseMenu)


@dp.message_handler(text='Выбрать упражнение')
async def choice_exercise(message: types.Message):
    user_data[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, f'Упражнение: {exercises[user_data[message.from_user.id]]}',
                           reply_markup=get_keyboard_training)


@dp.message_handler(text='Случайное упражнение')
async def random_exercise(message: types.Message):
    exercise = choice(exercises)
    f = open("exercises.txt", 'r', encoding='utf8')
    data = f.readlines()
    f.close()
    await bot.send_message(message.from_user.id, f'Упражнение: {exercise}\n{data[exercises.index(exercise)]}')


@dp.message_handler(text='Начать тренировку')
async def workout_start(message: types.Message):
    btn = types.InlineKeyboardButton(text="ДА!", callback_data="yes")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(btn)
    await bot.send_message(message.from_user.id, f'Начинаем?', reply_markup=keyboard)


# @dp.callback_query_handler(text='notification_completion_on')
# async def notification_completion_on(call: types.CallbackQuery):
#     await call.message.edit_text('Уведомления о завершении работы бота были включены')
#     cur.execute(f"UPDATE users SET completion_notification='True' "
#                 f"WHERE chat_id={call.from_user.id}")
#     connection.commit()


# @dp.callback_query_handler(text='notification_completion_off')
# async def notification_completion_off(call: types.CallbackQuery):
#     await call.message.edit_text('Уведомления о завершении работы бота были выключены')
#     cur.execute(f"UPDATE users SET completion_notification='False' "
#                 f"WHERE chat_id={call.from_user.id}")
#     connection.commit()


# @dp.callback_query_handler(text='notification_weather_on')
# async def notification_weather_on(call: types.CallbackQuery):
#     await call.message.edit_text('Уведомления о погоде были включены')
#     cur.execute(f"UPDATE users SET mailing='True' "
#                 f"WHERE chat_id={call.from_user.id}")
#     connection.commit()


# @dp.callback_query_handler(text='notification_weather_off')
# async def notification_weather_off(call: types.CallbackQuery):
#     await call.message.edit_text('Уведомления о погоде были выключены')
#     cur.execute(f"UPDATE users SET mailing='False' "
#                 f"WHERE chat_id={call.from_user.id}")
#     connection.commit()


@dp.callback_query_handler(text='yes')
async def yes(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardRemove()
    for i in range(5, 0, -1):
        await call.message.edit_text(str(i))
        sleep(1)
    f = open("exercises.txt", 'r', encoding='utf8')
    data = f.readlines()
    f.close()
    for i in exercises:
        await call.message.edit_text(f'Упражнение: {i}\n{data[exercises.index(i)]}')
        sleep(30)
    await call.answer()


# @dp.callback_query_handler(text='stop')
# async def countdown(call: types.CallbackQuery):
#     if call.from_user.id == 1212339097 or call.from_user.id == 1300485082:
#         await call.message.edit_text('Бот остановлен!')
#         await bot.answer_callback_query(call.id,
#                                         text='Бот был принудительно остановлен!'
#                                              ' Данное оповещение пришло всем пользователям.',
#                                         show_alert=True)
#         data = cur.execute(f"SELECT chat_id FROM users WHERE completion_notification='True'"
#                            ).fetchall()
#         for i in data:
#             await bot.send_message(*i, f'Бот был остановлен, извените за неудобства😔')
#         exit(0)
#
#     else:
#         await call.message.edit_text('У вас нет прав администратора!')


# @dp.callback_query_handler(text='back')
# async def countdown(call: types.CallbackQuery):
#     user_index = user_data[call.from_user.id]
#     try:
#         await call.message.edit_text(f'Упражнение: {exercises[user_index - 1]}', reply_markup=get_keyboard2())
#         user_data[call.from_user.id] = user_index - 1
#     except IndexError:
#         await call.message.edit_text(f'Упражнение: {exercises[11]}', reply_markup=get_keyboard2())
#         user_data[call.from_user.id] = 11
#     await call.answer()
#
#
# @dp.callback_query_handler(text='next')
# async def callbacks_next(call: types.CallbackQuery):
#     user_index = user_data[call.from_user.id]
#     try:
#         await call.message.edit_text(f'Упражнение: {exercises[user_index + 1]}', reply_markup=get_keyboard2())
#         user_data[call.from_user.id] = user_index + 1
#     except IndexError:
#         await call.message.edit_text(f'Упражнение: {exercises[0]}', reply_markup=get_keyboard2())
#         user_data[call.from_user.id] = 0
#     await call.answer()


# @dp.callback_query_handler(text='confirm')
# async def callbacks_confirm(call: types.CallbackQuery):
#     user_index = user_data[call.from_user.id]
#     f = open("exercises.txt", 'r', encoding='utf8')
#     data = f.readlines()
#     f.close()
#     await call.message.edit_text(f'Упражнение "{exercises[user_index]}"\n{data[user_index]}')
#     await call.answer()


executor.start_polling(dp, skip_updates=False)
