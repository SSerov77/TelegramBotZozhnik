from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

'''Клавиатура основного меню'''

# создаем кнопки основной клавиатуры
btnNutrition = KeyboardButton('Ваше питание')
btnTraining = KeyboardButton('Тренировки')
btnNotify = KeyboardButton('Уведомления')
btnAchievements = KeyboardButton('Ваши достижения')
btnOther = KeyboardButton('Другое')

# создаем маркап основной клавиутры
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.row(btnNutrition, btnTraining).row(btnNotify, btnAchievements, btnOther)

'''Клавиатура другого меню'''

# создаем кнопки дургой клавиатуры
btnWeather = KeyboardButton('Погода')
btnFacts = KeyboardButton('Интересные факты')
btnMotivation = KeyboardButton('Мотивация')
btnBack = KeyboardButton('Назад')

# создаем маркап другой клавиатуры
otherMunu = ReplyKeyboardMarkup(resize_keyboard=True)
otherMunu.row(btnWeather, btnFacts).row(btnMotivation, btnBack)
