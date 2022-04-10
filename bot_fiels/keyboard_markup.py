from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
