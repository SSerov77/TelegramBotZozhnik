'''Получение названий блюд'''


class Food:  # класс получения блюд
    def __init__(self, button):
        self.button = button  # определяем какую категорию выбрал юзер
        self.result = []  # список - результат
        self.food()  # вызов функции получения напзвания блюд

    def food(self):
        tot = []  # список категории
        res = []  # итоговый список меню
        with open("food_menu.txt", 'r', encoding='utf8') as f:  # открываем файл с названиями
            data = f.readlines()  # читаем файл
            for i in data:  # пробегаемся по строкам
                i = i.rstrip('\n')  # получаем строку в нормальном виде
                if i != '':  # если не пробел
                    tot.append(i)  # добавляем строку в категорию
                elif i == '':  # если пробел
                    res.append(tot)  # добавляем категорию в меню
                    tot = []  # очищаем категорию
            res.append(tot)  # итоговое меню
        if self.button == 'Салаты':  # если юзер выбрал салаты
            self.result = res[0]
        elif self.button == 'Супы':  # если юзер выбрал супы
            self.result = res[1]
        elif self.button == 'Горячее':  # если юзер выбрал горячее
            self.result = res[2]
        elif self.button == 'Рыба':  # если юзер выбрал рыбу
            self.result = res[3]
        elif self.button == 'Напитки':  # если юзер выбрал напитки
            self.result = res[4]
