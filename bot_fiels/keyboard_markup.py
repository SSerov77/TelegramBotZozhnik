from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

'''Основное меню'''

# создаем кнопки основной клавиатуры
btnNutrition = KeyboardButton('Правильное питание')
btnTraining = KeyboardButton('Тренировки')
btnNotify = KeyboardButton('Уведомления')
btnAchievements = KeyboardButton('Ваши достижения')
btnOther = KeyboardButton('Другое')

# создаем маркап основной клавиутры
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.row(btnNutrition, btnTraining).row(btnNotify, btnAchievements, btnOther)

'''Другое меню'''

# создаем кнопки дургой клавиатуры
btnWeather = KeyboardButton('Погода')
btnFacts = KeyboardButton('Интересные факты')
btnMotivation = KeyboardButton('Мотивация')
btnBack = KeyboardButton('Назад в главное меню')

# создаем маркап другой клавиатуры
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True)
otherMenu.row(btnWeather, btnFacts).row(btnMotivation, btnBack)

'''Погода'''

# создаем кнопки для раздела погода
btnCity = KeyboardButton('Узнать погоду')
btnOtherCity = KeyboardButton('Поменять город')
btnBack1 = KeyboardButton('Назад в "Другое"')

# создаем маркап для клавиатуры погоды
weatherMenu = ReplyKeyboardMarkup(resize_keyboard=True)
weatherMenu.row(btnCity, btnOtherCity, btnBack1)

'''Правильное питание'''

# создаем кнопки для раздела правильно питание цель
btnPurpose = KeyboardButton('Ваша цель')
btnOtherPurpose = KeyboardButton('Поменять цель')

# создаем кнопки для раздела правильно питание поменять цель
btnSalad = KeyboardButton('Салаты')
btnHotter = KeyboardButton('Горячее')
btnSoups = KeyboardButton('Супы')
btnFish = KeyboardButton('Рыба')
btnDrinks = KeyboardButton('Напитки')

# создаем маркап для клавиатуры правильного питания цель
purposeMenu = ReplyKeyboardMarkup(resize_keyboard=True)
purposeMenu.row(btnSoups, btnHotter, btnFish).row(btnSalad, btnDrinks).row(btnBack)

'''Уведомления'''

# создаем кнопки для раздале уведомления
btnAdd = KeyboardButton('Добавить')
btnDelete = KeyboardButton('Удалить')

# создаем маркап для уведомления
notifyMenu = ReplyKeyboardMarkup(resize_keyboard=True)
notifyMenu.row(btnAdd, btnDelete, btnBack)

'''Настройки'''

# создаем кнопки для раздале настройки
btnNotificationWeather = KeyboardButton('Уведомления погоды')
btnNotificationCompletion = KeyboardButton('Уведомление остановки бота')
btnBack = KeyboardButton('Назад в главное меню')

# создаем маркап для настроек
settingsMenu = ReplyKeyboardMarkup(resize_keyboard=True)
settingsMenu.row(btnNotificationWeather)
settingsMenu.row(btnNotificationCompletion)
settingsMenu.row(btnBack)

'''Тренировка'''

# создаем кнопки для раздале тренировок
btnStart = KeyboardButton('Начать тренировку')
btnRandomExercise = KeyboardButton('Случайное упражнение')
btnChoiceExercise = KeyboardButton('Выбрать упражнение')
btnBack = KeyboardButton('Назад в "Другое"')

# создаем маркап для тренировок
exerciseMenu = ReplyKeyboardMarkup(resize_keyboard=True)
exerciseMenu.row(btnStart, btnRandomExercise)
exerciseMenu.row(btnChoiceExercise, btnBack)


def get_keyboard_food():
    buttons = [
        types.InlineKeyboardButton(text="<<", callback_data="back"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="finish"),
        types.InlineKeyboardButton(text=">>", callback_data="up")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_training():
    buttons = [
        types.InlineKeyboardButton(text="<<", callback_data="back"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
        types.InlineKeyboardButton(text=">>", callback_data="next")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard
