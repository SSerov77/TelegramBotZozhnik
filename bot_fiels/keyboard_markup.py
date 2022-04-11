from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

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
btnStart = KeyboardButton('Начать тренировку')
btnRandomExercise = KeyboardButton('Случайное упражнение')
btnChoiceExercise = KeyboardButton('Выбрать упражнение')
btnBack = KeyboardButton('Назад в "Другое"')

# создаем маркап для тренировок
exerciseMenu = ReplyKeyboardMarkup(resize_keyboard=True)
exerciseMenu.row(btnStart, btnRandomExercise)
exerciseMenu.row(btnChoiceExercise, btnBack)

'''Редактирование пользователей'''

btnBackUser = types.InlineKeyboardButton(text="<<", callback_data="back_user")
btnNextUser = types.InlineKeyboardButton(text=">>", callback_data="next_user")
btnConfirmUser = types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm_user")
editingUsers = types.InlineKeyboardMarkup(row_width=3)
editingUsers.add(btnBackUser, btnConfirmUser, btnNextUser)

'''Выбор изменения'''

btnEditWeather = types.InlineKeyboardButton(text="Погода", callback_data="pass")
btnEditBot = types.InlineKeyboardButton(text="Отключение бота", callback_data="pass")
btnEditStatus = types.InlineKeyboardButton(text="Сделать администратором", callback_data="pass")
btnBack = types.InlineKeyboardButton(text="Назад", callback_data="pass")
choiceEdit = types.InlineKeyboardMarkup(row_width=2)
choiceEdit.add(btnEditWeather, btnEditBot)
choiceEdit.add(btnEditStatus, btnBack)