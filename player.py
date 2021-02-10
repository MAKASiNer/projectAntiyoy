from cell import Cell
from unit import Unit
from type import Type
from building import Building



class Player:
    def __init__(self, count=None):
        if count == None: self.count = 1
        else: self.count = count

        self.thisPl = 1             # текущий игрок
        self.moneyPl = [0, 0, 0, 0] # деньги игроков
        # ресурсы - провизия/дерево/камень
        self.resourcesPl = [           
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    ''' меняет игрока на следующего'''
    def nextPlaeyr(self):
        self.thisPl = self.thisPl % self.count + 1
        return self.thisPl
    
    ''' возращает текущего игрока'''
    def thisPlayer(self):
        return self.thisPl

    ''' деньги текущего игрока '''
    def money(self, add=0):
        self.moneyPl[self.thisPl - 1] += add
        return self.moneyPl[self.thisPl - 1]
    
    ''' ресурсы текущего игрока '''
    def resources(self, add=[0, 0, 0]):
        self.resourcesPl[self.thisPl - 1][0] += add[0]
        self.resourcesPl[self.thisPl - 1][1] += add[1]
        self.resourcesPl[self.thisPl - 1][2] += add[2]
        return self.resourcesPl[self.thisPl - 1]