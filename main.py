import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from bot_fiels import keyboard_markup as kb
from bot_fiels.food import Food, Recepts

from data import db_session
from data.users import User

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

user_data = {}
menu = []
dish = ''
total_id_users = []
user = User()


def main(id_user, name):
    db_sess = db_session.create_session()
    print(1)
    for i in db_sess.query(User).all():
        i = i.id_user
        if i not in total_id_users:
            total_id_users.append(i)
        if id_user not in total_id_users:
            print(total_id_users)
            user.name = name
            user.id_user = id_user
            db_sess.add(user)
            total_id_users.append(i)
            db_sess.commit()


def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="<", callback_data="backk"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="finish"),
        types.InlineKeyboardButton(text=">", callback_data="upp")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(text=['Супы', 'Салаты', 'Горячее', 'Рыба', 'Напитки'])
async def other_kb(message: types.Message):
    global menu
    global dish
    menu = Food(str(message.text)).result
    dish = str(message.text)
    user_data[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, f'Блюдо: {menu[user_data[message.from_user.id]]}',
                           reply_markup=get_keyboard())


@dp.callback_query_handler(text='backk')
async def countdown(call: types.CallbackQuery):
    global menu
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Блюдо: {menu[user_index - 1]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Блюдо: {menu[len(menu)]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = len(menu)
    await call.answer()


@dp.callback_query_handler(text='finish')
async def callbacks_confirm(call: types.CallbackQuery):
    global menu
    global dish
    user_index = user_data[call.from_user.id]
    result = Recepts(int(user_index), dish).result_dish
    await call.message.edit_text(f'{menu[user_index]}: '
                                 f'\n{result}')
    await call.answer()


@dp.callback_query_handler(text='upp')
async def countdown(call: types.CallbackQuery):
    global menu
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Блюдо: {menu[user_index + 1]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'Блюдо: {menu[0]}', reply_markup=get_keyboard())
        user_data[call.from_user.id] = 0
    await call.answer()


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}, если возникнут вопросы напиши \help',
                           reply_markup=kb.mainMenu)
    main(message.from_user.id, message.from_user.first_name)


@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
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


@dp.message_handler(text=['Уведомления'])
async def back_to_other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Погода"', reply_markup=kb.notifyMenu)


@dp.message_handler()
async def message_send(message: types.Message):
    pass


executor.start_polling(dp, skip_updates=False)
