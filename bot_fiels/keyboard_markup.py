from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # import aiogram
from aiogram import types

'''Основное меню'''

# создаем кнопки основной клавиатуры(меню)
btnNutrition = KeyboardButton('Правильное питание')
btnTraining = KeyboardButton('Тренировки')
btnAchievements = KeyboardButton('Блокнот')
btnOther = KeyboardButton('Другое')

# создаем маркап основной клавиутры
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.row(btnNutrition, btnTraining).row(btnAchievements, btnOther)

'''Другое меню'''

# создаем кнопки дургой клавиатуры
btnWeather = KeyboardButton('Погода')
btnFacts = KeyboardButton('Интересный факт')
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


def get_keyboard_food():
    buttons = [
        types.InlineKeyboardButton(text="<<", callback_data="down"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="finish"),
        types.InlineKeyboardButton(text=">>", callback_data="up")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


# создаем маркап для клавиатуры правильного питания
purposeMenu = ReplyKeyboardMarkup(resize_keyboard=True)
purposeMenu.row(btnSoups, btnHotter, btnFish).row(btnSalad, btnDrinks).row(btnBack)

'''Уведомления'''

# создаем маркап для уведомления
notifyMenu = ReplyKeyboardMarkup(resize_keyboard=True)
notifyMenu.row(btnBack)
btnAdd = types.InlineKeyboardButton(text="Добавить уведомление", callback_data="add_reminder")
reminderMenu = types.InlineKeyboardMarkup(row_width=1)
reminderMenu.add(btnAdd)

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

'''Дополнительные настройки администратора'''

settingsMenuAdmin = ReplyKeyboardMarkup(resize_keyboard=True)
btnNotificationUser = KeyboardButton('Уведомления пользователей')
settingsMenuAdmin.row(btnNotificationUser)
settingsMenuAdmin.row(btnNotificationWeather)
settingsMenuAdmin.row(btnNotificationCompletion)
settingsMenuAdmin.row(btnBack)

'''Тренировка'''

# создаем кнопки для раздале тренировок
btnRandomExercise = KeyboardButton('Случайное упражнение')
btnChoiceExercise = KeyboardButton('Выбрать упражнение')

# создаем маркап для тренировок
exerciseMenu = ReplyKeyboardMarkup(resize_keyboard=True)
exerciseMenu.row(btnRandomExercise)
exerciseMenu.row(btnChoiceExercise, btnBack)


def get_keyboard_training():  # функция создания клавитуры для тренировок
    buttons = [
        types.InlineKeyboardButton(text="<<", callback_data="back"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
        types.InlineKeyboardButton(text=">>", callback_data="next")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard  # возращаем клавиатуру


'''Редактирование пользователей'''

# создаем кнопки клавиатуры
btnBackUser = types.InlineKeyboardButton(text="<<", callback_data="back_user")
btnNextUser = types.InlineKeyboardButton(text=">>", callback_data="next_user")
btnConfirmUser = types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm_user")
# создаем маркап
editingUsers = types.InlineKeyboardMarkup(row_width=3)
editingUsers.add(btnBackUser, btnConfirmUser, btnNextUser)

'''Выбор изменения'''

# создаем кнопки для выбора изменений
btnEditWeather = types.InlineKeyboardButton(text="Погода", callback_data="weather")
btnEditBot = types.InlineKeyboardButton(text="Отключение бота", callback_data="disabling_bot")
btnEditStatus = types.InlineKeyboardButton(text="Сделать администратором", callback_data="admin")
btnBack = types.InlineKeyboardButton(text="Назад", callback_data="back_choice_user")
# создаем маркап
choiceEdit = types.InlineKeyboardMarkup(row_width=2)
choiceEdit.add(btnEditWeather, btnEditBot)
choiceEdit.add(btnEditStatus, btnBack)

'''Включить/выключить уведомления бота'''

btnChoiceOnOffDisablingBot = types.InlineKeyboardButton(text="Вкл/Выкл",
                                                        callback_data="on_off_disabling_bot")  # создаем кнопку Включить/выключить уведомления бота
# содаем маркап Включить/выключить уведомления бота
on_off_disabling_bot = types.InlineKeyboardMarkup(row_width=1)
on_off_disabling_bot.add(btnChoiceOnOffDisablingBot)

'''Вклюить/выключить уведомления погоды'''

btnChoiceOnOffWeather = types.InlineKeyboardButton(text="Вкл/Выкл",
                                                   callback_data="on_off_weather")  # создаем кнопку Включить/выключить уведомления погоды
# создаем маркап Включить/выключить уведомления погоды
on_off_weather = types.InlineKeyboardMarkup(row_width=1)
on_off_weather.add(btnChoiceOnOffWeather)

'''Включить/выключить права администратора'''

btnChoiceOnOffAdmin = types.InlineKeyboardButton(text="Вкл/Выкл",
                                                 callback_data="on_off_admin")  # создаем кнопку Включить/выключить права администратора
# создаем маркап Включить/выключить права администратора
on_off_admin = types.InlineKeyboardMarkup(row_width=1)
on_off_admin.add(btnChoiceOnOffAdmin)
