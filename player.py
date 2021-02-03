from cell import Cell
from unit import Unit
from type import Type
from building import Building



class Player:
    def __init__(self, count=None):
        if count == None: self.count = 1
        else: self.count = count

        self.thisPlayer = 1

    ''' меняет игрока на следующего'''
    def nextPlaeyr(self):
        self.thisPlayer = self.thisPlayer % self.count + 1
        return self.thisPlayer
    
    ''' возращает текущего игрока'''
    def thisPlayer(self):
        return self.thisPlayer