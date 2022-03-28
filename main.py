from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import sqlite3
import os
from random import choice
from bot_fiels import keyboard_markup as kb

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect('BotZozhnik.db')
cur = connection.cursor()


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


@dp.message_handler(text=['Поменять город'])
async def weather_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
                           reply_markup=kb.weatherMenu)


executor.start_polling(dp, skip_updates=True)
