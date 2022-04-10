from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import sqlite3
from time import sleep
import os
from random import choice
from bot_fiels import keyboard_markup as kb
from aiogram.types import ReplyKeyboardMarkup

from config import TOKEN
from bot_fiels import keyboard_markup as kb
from random import choice
from bot_fiels.weather import Weather

user_data = {}
exercises = ['Прыжки', 'Приседание у стены', 'Отжимания от пола', 'Подъемы на стул', 'Наклон вперед из положения лежа',
             'Приседания', 'Бег, колени вверх',
             'Выпады', 'Отжимания с поворотом', 'Боковая планка', 'Обратные отжимания от стула', 'Планка']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect('BotZozhnik.db')
cur = connection.cursor()

help_text = 'Как пользоваться ботом?' \
            '\n❗Чтобы вызвать клавиатуру основного меню, введи команду \start' \
            '\nПосле этого выбери один из нужных тебе инструментов' \
            '\n✅Раздел "Ваше питание" подскажет тебе нужный рацион чтобы похудеть, набрать массу или поддерживать её' \
            '\n✅Раздел "Тренировки" подскажет тебе быстрые и удобные физические упражнения на каждый день' \
            '\n✅В разделе "Мои достижения" ты можешь записывать свои успехи по улучшению себя' \
            '\n✅В разделе "Уведомления" ты можешь записать что-то и бот тебе это пришлёт несколько раз ,чтобы ты не забыл об этом' \
            '\n🔅Например, когда тебе нужно принять таблетки' \
            '\n✅В "Другое" ты найдешь еще много чего интересного:)'

def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="<<", callback_data="back"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
        types.InlineKeyboardButton(text=">>", callback_data="next")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard



@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    if not cur.execute(f'''select chat_id From users
                        where chat_id = '{message.chat.id}' ''').fetchall():
        cur.execute("INSERT INTO users(chat_id, name, weight, city, mailing, completion_notification)"
                    "VALUES(?, ?, ?, ?, ?, ?)",
                    (message.chat.id, str(message.from_user.first_name), None, None, 'False', 'True'))
        connection.commit()
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}, если возникнут вопросы напиши \help',
                           reply_markup=kb.mainMenu)


@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, help_text, reply_markup=kb.mainMenu)


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


@dp.message_handler(commands=['stop'])
async def command_start(message: types.Message):
    btn = types.InlineKeyboardButton(text="ДА!", callback_data="stop")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(btn)
    await bot.send_message(message.from_user.id, f'Вы действительно хотите остановить бота?', reply_markup=keyboard)


@dp.message_handler(commands=['settings'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в настройки',
                           reply_markup=kb.settingsMenu)


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


@dp.message_handler(text=['Ваш город'])
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
    f = open("quotes.txt", 'r', encoding="utf8")
    data = f.readlines()
    await bot.send_message(message.from_user.id, str(choice(data)))


# @dp.message_handler(text=['Поменять город'])
# async def weather_kb(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
#                            reply_markup=kb.weatherMenu)

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
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(btn)
    await bot.send_message(message.from_user.id, f'Начинаем?', reply_markup=keyboard)


@dp.callback_query_handler(text='notification_completion_on')
async def notification_completion_on(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о завершении работы бота были включены')
    cur.execute(f"UPDATE users SET completion_notification='True' "
                f"WHERE chat_id={call.from_user.id}")
    connection.commit()


@dp.callback_query_handler(text='notification_completion_off')
async def notification_completion_off(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о завершении работы бота были выключены')
    cur.execute(f"UPDATE users SET completion_notification='False' "
                f"WHERE chat_id={call.from_user.id}")
    connection.commit()


@dp.callback_query_handler(text='notification_weather_on')
async def notification_weather_on(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о погоде были включены')
    cur.execute(f"UPDATE users SET mailing='True' "
                f"WHERE chat_id={call.from_user.id}")
    connection.commit()


@dp.callback_query_handler(text='notification_weather_off')
async def notification_weather_off(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о погоде были выключены')
    cur.execute(f"UPDATE users SET mailing='False' "
                f"WHERE chat_id={call.from_user.id}")
    connection.commit()


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


@dp.callback_query_handler(text='stop')
async def countdown(call: types.CallbackQuery):
    if call.from_user.id == 1212339097 or call.from_user.id == 1300485082:
        await call.message.edit_text('Бот остановлен!')
        await bot.answer_callback_query(call.id,
                                        text='Бот был принудительно остановлен!'
                                             ' Данное оповещение пришло всем пользователям.',
                                        show_alert=True)
        data = cur.execute(f'''SELECT chat_id From users
                                WHERE completion_notification=True''').fetchall()
        for i in data:
            await bot.send_message(*i, f'Бот был остановлен, извените за неудобства😔')
        exit(0)
    else:
        await call.message.edit_text('У вас нет прав администратора!')


@dp.callback_query_handler(text='back')
async def countdown(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Упражнение: {exercises[user_index - 1]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Упражнение: {exercises[11]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = 11
    await call.answer()


@dp.callback_query_handler(text='next')
async def callbacks_next(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Упражнение: {exercises[user_index + 1]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'Упражнение: {exercises[0]}', reply_markup=get_keyboard())
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

@dp.message_handler()
async def message_send(message: types.Message):
    pass



executor.start_polling(dp, skip_updates=True)
