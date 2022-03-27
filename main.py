from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3

import os

bot = Bot(token=os.getenv('TOKEN'))
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


@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text)


executor.start_polling(dp, skip_updates=True)
