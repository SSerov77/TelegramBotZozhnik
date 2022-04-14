
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
        if self.button == 'Салаты':
            self.result = res[0]
        elif self.button == 'Супы':
            self.result = res[1]
        elif self.button == 'Рыба':
            self.result = res[2]
