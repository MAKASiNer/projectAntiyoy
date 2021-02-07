from cell import Cell
from unit import Unit
from type import Type
from building import Building



class Player:
    def __init__(self, count=None):
        if count == None: self.count = 1
        else: self.count = count

        self.thisPl = 1

    ''' меняет игрока на следующего'''
    def nextPlaeyr(self):
        self.thisPl = self.thisPl % self.count + 1
        return self.thisPl
    
    ''' возращает текущего игрока'''
    def thisPlayer(self):
        return self.thisPl