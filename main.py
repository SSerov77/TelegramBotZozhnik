from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import sqlite3
from time import sleep
import os
from random import choice
# from bot_fiels import keyboard_markup as kb
from aiogram.types import ReplyKeyboardMarkup

user_data = {}
exercises = ['Прыжки', 'Приседание у стены', 'Отжимания от пола', 'Подъемы на стул', 'Наклон вперед из положения лежа', 'Приседания', 'Бег, колени вверх',
             'Выпады', 'Отжимания с поворотом', 'Боковая планка', 'Обратные отжимания от стула', 'Планка']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect('BotZozhnik.db')
cur = connection.cursor()

def get_keyboard(index=0):
    buttons = [
        types.InlineKeyboardButton(text="<<", callback_data="back"),
        types.InlineKeyboardButton(text=exercises[index], callback_data="None"),
        types.InlineKeyboardButton(text=">>", callback_data="next"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    if not cur.execute(f'''select chat_id From users
                        where chat_id = '{message.chat.id}' ''').fetchall():
        cur.execute("INSERT INTO users(chat_id, name, weight, city)"
                    "VALUES(?, ?, ?, ?)",
                    (message.chat.id, str(message.from_user.first_name), None, None))
        connection.commit()


@dp.message_handler(commands=['choicecity'])
async def command_start(message: types.Message):
    try:
        new_city = message.get_args()
        cur.execute(f"UPDATE users SET city='{new_city}' "
                    f"WHERE chat_id={message.from_user.id}")
        connection.commit()
    except:
        await bot.send_message(message.from_user.id, 'Некоректный запрос')
    else:
        await bot.send_message(message.from_user.id, f'Ваш город был изменён на: {new_city}')


@dp.message_handler(text='Мотивация')
async def quotes(message: types.Message):
    f = open("quotes.txt", 'r', encoding="utf8")
    data = f.readlines()
    await bot.send_message(message.from_user.id, str(choice(data)))


# @dp.message_handler(text=['Поменять город'])
# async def weather_kb(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
#                            reply_markup=kb.weatherMenu)


@dp.message_handler(text='Тренировки')
async def workout(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['Начать тренировку', 'Случайное упражнение'])
    keyboard.add(*['Выбрать упражнение', 'Назад в "Другое"'])
    await bot.send_message(message.from_user.id, 'Вы перешли в раздел "Тренировки", введите команду или выберите из предложенных',
                           reply_markup=keyboard)


@dp.message_handler(text='Выбрать упражнение')
async def choice_exercise(message: types.Message):
    user_data[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, 'Выберите упражнение:',
                           reply_markup=get_keyboard())


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
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(btn)
    await bot.send_message(message.from_user.id, f'Начинаем?', reply_markup=keyboard)



@dp.callback_query_handler(text='yes')
async def yes(call: types.CallbackQuery):
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



@dp.callback_query_handler(text='back')
async def countdown(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Выберите упражнение:', reply_markup=get_keyboard(user_index - 1))
        user_data[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Выберите упражнение:', reply_markup=get_keyboard(11))
        user_data[call.from_user.id] = 11
    await call.answer()



@dp.callback_query_handler(text='back')
async def callbacks_bcak(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Выберите упражнение:', reply_markup=get_keyboard(user_index - 1))
        user_data[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Выберите упражнение:', reply_markup=get_keyboard(11))
        user_data[call.from_user.id] = 11
    await call.answer()


@dp.callback_query_handler(text='next')
async def callbacks_next(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Выберите упражнение:', reply_markup=get_keyboard(user_index + 1))
        user_data[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'Выберите упражнение:', reply_markup=get_keyboard(0))
        user_data[call.from_user.id] = 0
    await call.answer()


@dp.callback_query_handler(text='confirm')
async def callbacks_confirm(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    f = open("exercises.txt", 'r', encoding='utf8')
    data = f.readlines()
    f.close()
    await call.message.edit_text(f'Упражнение "{exercises[user_index]}"\n{data[user_index]}')
    await call.answer()

executor.start_polling(dp, skip_updates=True)
