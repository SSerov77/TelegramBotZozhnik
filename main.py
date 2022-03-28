from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import sqlite3
import os
from random import choice

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect('BotZozhnik.db')
cur = connection.cursor()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    if not cur.execute(f'''select chat_id From users
                        where chat_id = '{message.chat.id}' ''').fetchall():
        cur.execute("INSERT INTO users(chat_id, name, weight, city)"
                    "VALUES(?, ?, ?, ?)",
                    (message.chat.id, str(message.from_user.first_name), None, None))
        connection.commit()


@dp.message_handler(text='Мотивация')
async def quotes(message: types.Message):
    f = open("quotes.txt", 'r', encoding="utf8")
    data = f.readlines()
    await bot.send_message(message.from_user.id, str(choice(data)))


executor.start_polling(dp, skip_updates=True)
