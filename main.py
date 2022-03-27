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
            '\n✅В "Другое" ты найдешь еще много чего интересного:)'


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}, возникнут вопросы напиши \help',
                           reply_markup=kb.mainMenu)


@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, help_text, reply_markup=kb.mainMenu)


@dp.message_handler()
async def message_send(message: types.Message):

    # Раздел другое
    if message.text == 'Другое':
        await bot.send_message(message.from_user.id, 'Вы перешли в "Другое"', reply_markup=kb.otherMenu)
    elif message.text == 'Назад в главное меню':
        await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=kb.mainMenu)

    # Функционал кнопок в разделе Правильное питание
    elif message.text == 'Правильное питание':
        await bot.send_message(message.from_user.id, 'Правильное питание', reply_markup=kb.purposeMenu)
    elif message.text == 'Поменять цель':
        await bot.send_message(message.from_user.id, 'Вы решили изменить свою цель', reply_markup=kb.getPurposeMenu)
    elif message.text == 'Назад в "Правильное питание"':
        await bot.send_message(message.from_user.id, 'Вы вернусь в "Правильное питание"',
                               reply_markup=kb.purposeMenu)

    elif message.text == 'Поменять цель':
        await bot.send_message(message.from_user.id, 'Вы решили поменять цель',
                               reply_markup=kb.getPurposeMenu)
    # Функционал кнопок разделе Погода
    elif message.text == 'Погода':
        await bot.send_message(message.from_user.id, 'Вы перешли в "Погода"', reply_markup=kb.weatherMenu)
    elif message.text == 'Назад в "Другое"':
        await bot.send_message(message.from_user.id, 'Вы вернулись в "Другое"', reply_markup=kb.otherMenu)

    # Функционал кнопок в разделе Уведомления
    elif message.text == 'Уведомления':
        await bot.send_message(message.from_user.id, 'Вы перешли в "Погода"', reply_markup=kb.notifyMenu)


executor.start_polling(dp, skip_updates=False)
