import datetime
import time
from random import choice  # рандом
import asyncio  # Импорт aioshedule
import aioschedule

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher  # Импорт aiogram
from aiogram.utils import executor

from data.config import TOKEN  # импорт токена бота

from bot_fiels.keyboard_markup import get_keyboard_food, get_keyboard_training  # импорт inline клавиатур
from bot_fiels import keyboard_markup as kb  # импорт клавиатур телеграмма

from data import db_session  # работа с БД
from data.db_session import global_init  # импорт функции создания БД
from data.other_data import facts, quots, help_text, exercises, exer  # импорт дополнительных данных

from bot_fiels.weather import Weather  # импорт класса погоды
from bot_fiels.food import Food  # импорт класса правильного питания
from data_tables.users_table import User  # импорт таблицы юзера из БД
from bot_fiels.send_photo import Photo  # импорт класса отправки фото

bot = Bot(token=TOKEN)  # создание бота
dp = Dispatcher(bot)  # создание диспетчер бота

user_data = {}  # создание множества с тренировками
user_data_dish = {}  # создание множества по правильному питанию
menu = []  # создание мписка меню
time_reminder = {}  # создание времени напоминалки
admin_user_data = []  # создание списка данных админа

global_init("db/database.db")  # подключение к БД
db_sess = db_session.create_session()  # создание сессии БД

'''Пользователь'''


def register(chat_id, name):  # функции рекгистрации пользоваеля в БД
    user = User()  # объявляем класс пользователя
    res = db_sess.query(User).filter(User.chat_id == chat_id).all()  # Находим этого пользователя
    if not res:  # проверем есть ли пользователь в БД
        user.name = name  # вводим в БД его имя
        user.chat_id = chat_id  # вводим в БД его id
        user.completion_notification = 'True'  # автоматическое согласение на отпраку уведомлений
        user.mailing = 'True'  # автоматичесмкое согласение на отправку уведомлений
        user.admin = 'False'  # автоматическое присваивание НЕ АДМИН
        user.city = ''  # указываем город(нет)
        db_sess.add(user)  # добавляем данные
        db_sess.commit()  # сохраняем даные


def update_data():  # функция обновления данных пользователя
    global admin_user_data  # объявляем глобальную переменную о данных для админа
    data = db_sess.query(User).all()  # берем всех пользователей из БД
    for i in data:  # пробегаемся по всем пользователям в БД
        id = i.chat_id  # находим их id
        name = i.name  # находим их имена
        city = i.city  # находим их города
        mail = i.mailing  # находим уведомления
        comp = i.completion_notification  # находим уведмления
        tot = [id, name, city, mail, comp]  # добавляем всё в список
        admin_user_data.append(tot)  # добавляем в информации для админа


@dp.message_handler(commands=['start'])  # функция /start (начальная команда)
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}, если возникнут вопросы напиши /help',
                           reply_markup=kb.mainMenu)  # выводим текст при вызове команды
    register(message.from_user.id, message.from_user.first_name)  # вызываем функцию регистрации пользователя #


@dp.message_handler(commands=['help'])  # функция /help
async def command_start(message: types.Message):
    global menu
    await bot.send_message(message.from_user.id, help_text,
                           reply_markup=kb.mainMenu)  # отправляем текст помощи пользователю


@dp.message_handler(commands=['settings'])  # функция /settings
async def command_start(message: types.Message):
    res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # находим пользователя в БД по id
    if res.admin == 'True':  # проверка на админа
        await bot.send_message(message.from_user.id, 'Вы перешли в настройки',  # клавиатура если админ
                               reply_markup=kb.settingsMenuAdmin)
    else:
        await bot.send_message(message.from_user.id, 'Вы перешли в настройки',  # клавиатура если НЕ админ
                               reply_markup=kb.settingsMenu)


'''Переключение между клавиатурами'''


@dp.message_handler(text=['Другое'])  # функция при нажатии на кнопку ДРУГОЕ
async def other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Другое"', reply_markup=kb.otherMenu)


@dp.message_handler(text=['Назад в "Другое"'])  # функция при нажатии на кнопку НАЗАД В ДРУГОЕ
async def back_to_other_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в "Другое"', reply_markup=kb.otherMenu)


@dp.message_handler(text=['Назад в главное меню'])  # функция при нажатии на кнопку НАЗАД В ГЛАВНОЕ МЕНЮ
async def nutrition_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=kb.mainMenu)


'''Правильное питание'''


@dp.message_handler(text=['Правильное питание'])  # кнопка ПРАВЛЬНОЕ ПИТАНИЕ
async def main_menu_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Правильное питание', reply_markup=kb.purposeMenu)


@dp.message_handler(text=['Назад в "Правильное питание"'])  # кнопка НАЗАД В ПРАВИЛЬНОЕ ПИТАНИЕ
async def nutrition_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернусь в "Правильное питание"',
                           reply_markup=kb.purposeMenu)


@dp.message_handler(text=['Супы', 'Салаты', 'Горячее', 'Рыба', 'Напитки'])  # проверяем что выбрал пользователь из меню
async def other_kb(message: types.Message):
    global menu  # выываем глобальную переменную меню
    menu = Food(str(message.text)).result  # получаем список блюд из выбранной категории
    user_data_dish[message.from_user.id] = 0  # ставим 0 индекс
    await bot.send_message(message.from_user.id, f'Найдем что-то вкусненькое?',
                           reply_markup=types.ReplyKeyboardRemove())  # удаляем клавиатуру
    await bot.send_message(message.from_user.id, f'Блюдо: {menu[user_data_dish[message.from_user.id]]}',
                           reply_markup=get_keyboard_food())  # начинаем листать блюда (вызываем inline клавиатуру)


@dp.callback_query_handler(text='up')  # если пользователь нажал ДАЛЬШЕ
async def countdown(call: types.CallbackQuery):
    global menu
    user_index = user_data_dish[call.from_user.id]  # получем id пользователя
    try:
        await call.message.edit_text(f'Блюдо: {menu[user_index + 1]}',
                                     reply_markup=get_keyboard_food())  # меняем на следующее блюдо
        user_data_dish[call.from_user.id] = user_index + 1
    except IndexError:
        await call.message.edit_text(f'Блюдо: {menu[0]}',
                                     reply_markup=get_keyboard_food())  # если кончился список возращаемся к 0 индексу
        user_data_dish[call.from_user.id] = 0
    await call.answer()


@dp.callback_query_handler(text='down')  # если пользователь нажал НАЗАД
async def countdown(call: types.CallbackQuery):
    global menu
    user_index = user_data_dish[call.from_user.id]  # получем id пользователя
    try:
        await call.message.edit_text(f'Блюдо: {menu[user_index - 1]}',
                                     reply_markup=get_keyboard_food())  # меняем на предыдущее блюдо
        user_data_dish[call.from_user.id] = user_index - 1
    except IndexError:
        await call.message.edit_text(f'Блюдо: {menu[len(menu)]}', reply_markup=get_keyboard_food())
        user_data_dish[call.from_user.id] = len(menu)  # если кончился список возращаемся к последнему индексу
    await call.answer()


@dp.callback_query_handler(text='finish')  # если пользователь нажал ПОДТВЕРДИТЬ
async def callbacks_confirm(call: types.CallbackQuery):
    global menu
    user_index = user_data_dish[call.from_user.id]  # получаем id
    result = Photo(menu[user_index]).photo  # получаем фото блюда
    result2 = Photo(menu[user_index]).photo2  # получаем фото рецепта блюда
    await call.message.answer_photo(photo=result)  # отправялем 1 фото
    await call.message.answer_photo(photo=result2,
                                    reply_markup=kb.purposeMenu)  # отправляем 2 фото и возращаем клавиатуру
    await call.answer()


'''Тренировки'''


@dp.message_handler(text='Тренировки')  # функция при нажатии на кнопку ТРЕНИРОВКИ
async def workout(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Вы перешли в раздел "Тренировки", введите команду или выберите из предложенных',
                           reply_markup=kb.exerciseMenu)


@dp.message_handler(text='Случайное упражнение')  # функция СЛУЧАЙНОЕ УПРАЖЕНЕНИЕ
async def random_exercise(message: types.Message):
    exercise = choice(exercises)  # выбираем рандомное упражнение
    data = exer  # описание упражнения
    await bot.send_message(message.from_user.id,
                           f'Упражнение: {exercise}\n{data[exercises.index(exercise)]}')  # отрпавляем его


@dp.message_handler(text='Выбрать упражнение')  # функция ВЫБОР УПРАЖНЕНИЯ
async def choice_exercise(message: types.Message):
    user_data[message.from_user.id] = 0
    await bot.send_message(message.from_user.id, 'Потренируемся!',
                           reply_markup=types.ReplyKeyboardRemove())  # удаляем клавиатуру
    await bot.send_message(message.from_user.id, f'Упражнение: {exercises[user_data[message.from_user.id]]}',
                           reply_markup=get_keyboard_training())  # вызываем inline клавиатуру с тренировками


@dp.callback_query_handler(text='back')  # если пользователь нажал НАЗАД
async def back(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Упражнение: {exercises[user_index - 1]}',
                                     reply_markup=get_keyboard_training())  # меняем на предыдущее упражнение
        user_data[call.from_user.id] = user_index - 1  # меняем ндекс списка
    except IndexError:
        await call.message.edit_text(f'Упражнение: {exercises[11]}',
                                     reply_markup=get_keyboard_training())  # если начальное значение меняем на последнее упражнение
        user_data[call.from_user.id] = 11  # меняем на последний индекс
    await call.answer()


@dp.callback_query_handler(text='next')  # если пользователь нажал ВПЕРЕД
async def callbacks_next(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    try:
        await call.message.edit_text(f'Упражнение: {exercises[user_index + 1]}',
                                     reply_markup=get_keyboard_training())  # меняем на след упржнение
        user_data[call.from_user.id] = user_index + 1  # меняем индекс списка
    except IndexError:
        await call.message.edit_text(f'Упражнение: {exercises[0]}',
                                     reply_markup=get_keyboard_training())  # если конечное значение меняем на первое упражнение
        user_data[call.from_user.id] = 0  # меняем на 0 индекс
    await call.answer()


@dp.callback_query_handler(text='confirm')  # если нажал подтвердить
async def confirm(call: types.CallbackQuery):
    user_index = user_data[call.from_user.id]
    data = exer
    await call.message.edit_text(f'Упражнение: {exercises[user_index]}\n{data[user_index]}')  # отравляем упражнение
    await call.message.answer(f'Удачной тренировки!', reply_markup=kb.exerciseMenu)  # возращаем клавиатуру
    await call.answer()


'''Погода'''


@dp.message_handler(text=['Погода'])  # при нажатии на кнопку ПОГОДА
async def weather_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы перешли в "Погода"', reply_markup=kb.weatherMenu)


@dp.message_handler(text=['Узнать погоду'])  # функция УЗНАТЬ ПОГОДУ
async def weather_kb(message: types.Message):
    res = Weather(str(message.chat.id)).result  # получаем резульат погоды
    if res:  # проверка результата
        await bot.send_message(message.from_user.id, res, reply_markup=kb.weatherMenu)  # если результат положительный
    else:
        await bot.send_message(message.from_user.id, f'Вы не ввели город',
                               reply_markup=kb.weatherMenu)  # если результат отрицательный


@dp.message_handler(text=['Поменять город'])  # при нажатии на ПОМЕНЯТЬ ГОРОД
async def weather_kb(message: types.Message):
    await bot.send_message(message.from_user.id, 'Чтобы изменить город введите "/choicecity <<Ваш город>>"',
                           reply_markup=kb.weatherMenu)


@dp.message_handler(commands=['choicecity'])  # функция /choicecity
async def command_start(message: types.Message):
    try:
        new_city = message.get_args()  # получаем новый город
        new_city = new_city.rstrip().lstrip()  # обрабатываем строку
        if new_city == '':  # проверка строки (результата)
            await bot.send_message(message.from_user.id, 'Вы ввели некорректный город')  # если результат пустой
        else:
            res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # если положительный
            res.city = new_city  # объявляем новый город пользователя
            db_sess.commit()  # сохранем в БД
            await bot.send_message(message.from_user.id, f'Ваш город был изменён на: {new_city}')
    except:
        await bot.send_message(message.from_user.id, 'Вы ввели некорректный город')


'''Мотивация и Факты'''


@dp.message_handler(text='Мотивация')  # при нажатии на МОТИВАЦИЯ
async def quotes(message: types.Message):
    await bot.send_message(message.from_user.id, str(choice(quots)),
                           reply_markup=kb.otherMenu)  # отпраляем рандомную цитату


@dp.message_handler(text='Интересные факты')  # при нажатии на ИНТРЕСНЫЕ ФАКТЫ
async def quotes(message: types.Message):
    await bot.send_message(message.from_user.id, str(choice(facts)),
                           reply_markup=kb.otherMenu)  # отправляем рандомный факт


'''Уведомления пользователей'''


@dp.message_handler(text='Уведомление остановки бота')  # функция уведомления об останвоки бота в случае остановки
async def notification_completion(message: types.Message):
    btn = types.InlineKeyboardButton(text="Включить", callback_data="notification_completion_on")  # inline кнопка вкл
    btn1 = types.InlineKeyboardButton(text="Выключить",
                                      callback_data="notification_completion_off")  # inline кнопка выкл
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # создаем маркап
    keyboard.add(btn, btn1)  # создаем клавиатуру
    await bot.send_message(message.from_user.id, f'Уведомление остановки бота', reply_markup=keyboard)


@dp.message_handler(text='Уведомления погоды')  # уведмоления об рассылки погоды
async def notification_weather(message: types.Message):
    btn = types.InlineKeyboardButton(text="Включить", callback_data="notification_weather_on")  # inline кнопка вкл
    btn1 = types.InlineKeyboardButton(text="Выключить", callback_data="notification_weather_off")  # inline кнопка выкл
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # создаем маркап
    keyboard.add(btn, btn1)  # создаем клавиатуру
    await bot.send_message(message.from_user.id, f'Уведомления погоды', reply_markup=keyboard)


@dp.message_handler(text='Уведомления пользователей')  # функция для админа (вкл\выкл уведомлений пользователя)
async def notification_weather(message: types.Message):
    res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # получаем пользователя по id из БД
    if res.admin == 'True':  # проверка на админа
        update_data()  # вызваем функцию обновления данных
        user_data[message.from_user.id] = 0
        await bot.send_message(message.from_user.id, f'Выберите пользователя:',
                               reply_markup=kb.editingUsers)  # если админ
    else:
        await bot.send_message(message.from_user.id, 'У вас нет прав администратора!')  # если НЕ админ


@dp.callback_query_handler(text='notification_completion_on')  # функция вкючения уведомлений
async def notification_completion_on(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о завершении работы бота были включены')
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()  # получаема юзера по id из БД
    res.completion_notification = 'True'  # ставим True на уведомления пользователя в БД
    db_sess.commit()  # сохраняем БД


@dp.callback_query_handler(text='notification_completion_off')  # функция выключения уведмолений
async def notification_completion_off(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о завершении работы бота были выключены')
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()  # получаем юзера по id из БД
    res.completion_notification = 'False'  # ставим False на уведомления юзера в БД
    db_sess.commit()  # сохраянем БД


@dp.callback_query_handler(text='notification_weather_on')  # функция включения уведомлений погоды
async def notification_weather_on(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о погоде были включены')  # менющийся текст
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()  # получаем юзера по id из БД
    res.mailing = 'True'  # ставим True на уведомления юзера в БД
    db_sess.commit()  # сохраняем БД


@dp.callback_query_handler(text='notification_weather_off')  # функция выключения увдомлений погоды
async def notification_weather_off(call: types.CallbackQuery):
    await call.message.edit_text('Уведомления о погоде были выключены')  # менющийся текст
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()  # получаем юзера по id из БД
    res.mailing = 'False'  # ставим False на уведомления юзера в БД
    db_sess.commit()  # сохраняем БД


'''Функционал Админа'''


@dp.message_handler(commands=['stop'])  # команда /stop
async def command_start(message: types.Message):
    res = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # получаем юзера из БД по id
    if res.admin == 'True':  # проверка на админа
        btn = types.InlineKeyboardButton(text="ДА!", callback_data="stop")  # появляется inline клавиатура
        keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем маркап
        keyboard.add(btn)  # добавляем клавиатуру
        await bot.send_message(message.from_user.id, f'Вы действительно хотите остановить бота?',
                               reply_markup=keyboard)  # уточняем действие


@dp.callback_query_handler(text='stop')  # функция stop
async def stop(call: types.CallbackQuery):
    res = db_sess.query(User).filter(User.chat_id == call.from_user.id).first()  # получаем юзера из БД по id
    if res.admin == 'True':  # проверка на админа
        await call.message.edit_text('Бот остановлен!')  # сообщение если админ
        await bot.answer_callback_query(call.id,
                                        text='Бот был принудительно остановлен!'
                                             ' Данное оповещение пришло всем пользователям.',
                                        show_alert=True)  # уточнение остановик бота
        data = db_sess.query(User).filter(
            User.completion_notification == 'True').all()  # получаем юзеров из БД по включению уведомлений
        for i in data:  # пробегаемся по всем пользователям
            i = i.chat_id  # получаем id юзера
            await bot.send_message(i, f'Бот был остановлен, извените за неудобства😔')  # рассылка сообщений
        exit(0)  # завершение работы бота
    else:
        await call.message.edit_text('У вас нет прав администратора!')  # если НЕ админ


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
    user_index = user_data[call.from_user.id]
    id = admin_user_data[user_index][0]
    res = db_sess.query(User).filter(User.chat_id == id).first()
    if res.mailing == 'True':
        res.mailing = 'False'
    else:
        res.mailing = 'True'
    db_sess.commit()


'''Блокнот'''


@dp.message_handler(text='Блокнот')  # функция при нажатии на кнопку БЛОКНОТ
async def workout(message: types.Message):
    try:
        data = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # получем данные юзера
        if not data.data_text or data.data_text == '':  # проверка его записей
            await bot.send_message(message.from_user.id, 'У вас нет записей!')  # если записей нет
        else:
            await bot.send_message(message.from_user.id, f'Ваши записи:\n{data.data_text}')  # если записи есть
        await bot.send_message(message.from_user.id,
                               'Введи чтобы:\nДобавить запись /add <Запись>\nУдалить запись /del <Номер записи>')
    except Exception:
        await bot.send_message(message.from_user.id,
                               'Произошла ошибка, приносим свои извинения!')


@dp.message_handler(commands='add')  # команда /add
async def workout(message: types.Message):
    try:
        data = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # получем данные пользователя
        if not data.data_text or data.data_text == '':  # проверка его записей\
            if message.text[5:] != '':  # Проверка на пустую запись
                data.data_text = f'{message.text[5:]}'  # получаем добавленую запись если первая и не пустая
            else:
                await bot.send_message(message.from_user.id,  # если пустая
                                       'Вы добавляете пустую запись!')
        else:
            data.data_text += f'\n{message.text[5:]}'  # получаем добавленую запись если не первая
        db_sess.commit()  # сохраняем БД
        await bot.send_message(message.from_user.id, 'Запись была добавлено!')  # сообщение об успешном добавлении
    except Exception:
        await bot.send_message(message.from_user.id,
                               'Произошла ошибка, приносим свои извинения!')


@dp.message_handler(commands='del')  # команда /del
async def workout(message: types.Message):
    try:
        data = db_sess.query(User).filter(User.chat_id == message.from_user.id).first()  # получем данные пользователя
        if data.data_text:
            res = [i for i in data.data_text.split('\n')]  # получаем список всех записей
            tot = int(message.text.split()[-1])  # получаем индекс записи, которую нужно удалить
            if tot > 0 and tot <= len(res):  # проверяем на индекс записи
                del res[tot - 1]  # удаляем
                data.data_text = None  # обновляем записи пользователя
                for i in res:  # пробегаемся по старым записям
                    if not data.data_text:  # если запись первая
                        data.data_text = f'{i}'
                    else:
                        data.data_text += f'\n{i}'  # если не первая
                db_sess.commit()  # сохраняем
                await bot.send_message(message.from_user.id, 'Запись была удалена!')  # сообщение об успешном удалении
            else:
                await bot.send_message(message.from_user.id,
                                       'Записи с таким номером не найдено')  # сообщение об успешном удалении
        else:
            await bot.send_message(message.from_user.id,
                                   'Записи с таким номером не найдено')  # сообщение об успешном удалении
    except Exception:
        await bot.send_message(message.from_user.id,
                               'Произошла ошибка, приносим свои извинения!')


# '''Напоминания'''
#
#
# @dp.message_handler(text=['Напоминания'])  # при нажатии на НАПОМИНАНИЯ
# async def back_to_other_kb(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Вы перешли в "Напомнить"',
#                            reply_markup=kb.notifyMenu)  # не реализровано
#     await bot.send_message(message.from_user.id, 'Напомнить', reply_markup=kb.reminderMenu)  # не реализровано
#
#
# @dp.callback_query_handler(text='add_reminder')  # не реализовано
# async def add_reminder(call: types.CallbackQuery):
#     await call.message.edit_text(
#         'Напишите, что и в какое время Вам напомнить.\n/reminder: <Напоминание>> <<время>> <')  # не реализовано
#
#
# @dp.message_handler(commands=['reminder'])  # не реализовано
# async def reminder_add(message: types.Message):  # не реализовано
#     text = message.text[10:].split()  # не реализовано
#     time = text[-1]  # не реализовано
#     text = " ".join(text[:-1])  # не реализовано
#
#
# async def mailing(text, time):
#     asyncio.create_task(reminder_add(mailing(text, time)))
#     now_time = str(datetime.datetime.now())[11:16]
#     if time == now_time:
#         await bot.send_message(message.from_user.id, f'Вы хотели {text}', reply_markup=kb.mainMenu)


'''Погода каждое утро'''


async def morning_weather():  # функция рассылки погоды кажое утро
    try:
        data = db_sess.query(User).filter(
            User.mailing == 'True').all()  # получаем всех юзеров из БД с вкл уведмолениями
        for i in data:  # пробегаемся по всем найденым юзерам
            i = i.chat_id  # получаем id юзера
            res = Weather(str(i)).result  # получаем результат погоды
            if res:  # проверка результата
                await bot.send_message(i, res, reply_markup=kb.weatherMenu)  # присылаем погоду
            else:
                await bot.send_message(i, f'Введите город, чтобы мы вам могли присылать погоду',
                                       reply_markup=kb.weatherMenu)  # если нет города
    except TypeError:
        await bot.send_message(i, f'Введите город, чтобы мы вам могли присылать погоду',
                               reply_markup=kb.weatherMenu)  # при ошибке если города нет


async def scheduler():  # функция отслеживания времени
    try:
        aioschedule.every().day.at("08:00").do(morning_weather)  # проверка времени и срабаотываение функции
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except TypeError:
        print(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


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

# @dp.callback_query_handler(text='on_off_admin')
# async def on_off_admin(call: types.CallbackQuery):
#     pass
#
#
# @dp.message_handler()
# async def error_message(message: types.Message):
#     # if ':' in message.text[0:4] and ' ' in message.text[3:5]:
#     #     time, np = message.text.split()
#     #     try:
#     #         time_reminder[time][chat_id] = np
#     #     except:
#     #         time_reminder[time] = {chat_id: np}
#     await bot.send_message(message.from_user.id, 'Я Вас не понимаю.', reply_markup=kb.reminderMenu)
