import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from bot_fiels import keyboard_markup as kb

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

help_text = 'Как пользоваться ботом?' \
            '\n❗Чтобы вызвать клавиатуру основного меню, введи команду \start' \
            '\nПосле этого выбери один из нужных тебе инструментов' \
            '\n✅Раздел "Ваше питание" подскажет тебе нужный рацион чтобы похудеть, набрать массу или поддерживать её' \
            '\n✅Раздел "Тренировки" подскажет тебе быстрые и удобные физические упражнения на каждый день' \
            '\n✅В разделе "Мои достижения" ты можешь записывать свои успехи по улучшению себя' \
            '\n✅В разделе "Уведомления" ты можешь записать что-то и бот тебе это пришлёт несколько раз ,чтобы ты не забыл об этом' \
            '\n🔅Например, когда тебе нужно принять таблетки' \
            '\n✅В "Другое" ты найдешь еще много чего интересного:)' \



@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}, возникнут вопросы напиши \help', reply_markup=kb.mainMenu)


@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, help_text, reply_markup=kb.mainMenu)


@dp.message_handler()
async def message_send(message: types.Message):
    if message.text == 'Другое':
        await bot.send_message(message.from_user.id, 'Раздел другое', reply_markup=kb.otherMunu)
    elif message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Вернуться назад', reply_markup=kb.mainMenu)


executor.start_polling(dp, skip_updates=False)
