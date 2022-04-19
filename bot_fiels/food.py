class Food:
    def __init__(self, button):
        self.button = button
        self.result = []
        self.food()

    def food(self):
        tot = []
        res = []
        f = open("food_menu.txt", 'r', encoding='utf8')
        data = f.readlines()
        for i in data:
            i = i.rstrip('\n')
            if i != '':
                tot.append(i)
            elif i == '':
                res.append(tot)
                tot = []
        res.append(tot)
        f.close()
        if self.button == 'Салаты':
            self.result = res[0]
        elif self.button == 'Супы':
            self.result = res[1]
        elif self.button == 'Горячее':
            self.result = res[2]
        elif self.button == 'Рыба':
            self.result = res[3]
        elif self.button == 'Напитки':
            self.result = res[4]


class Recepts:
    def __init__(self, index_menu, dish):
        self.index_menu = index_menu
        self.dish = dish
        self.result_dish = ''
        self.recept()

    def recept(self):
        if self.dish == 'Салаты':
            self.choose('salats.txt')
        elif self.choose == 'Супы':
            self.choose('soups.txt')
        elif self.dish == 'Горячее':
            self.choose('meat.txt')
        elif self.dish == 'Рыба':
            self.choose('fish.txt')
        elif self.dish == 'Напитки':
            self.choose('drink.txt')

    def choose(self, name):
        res = []
        with open(f'{name}', 'r', encoding='utf8') as f:
            data = f.readlines()
            tot = ''
            for i in data:
                i = i.rstrip('\n')
                if i != '':
                    tot += i
                elif i == '':
                    res.append(tot)
                    tot = ''
            res.append(tot)
        self.result_dish = res[self.index_menu]
