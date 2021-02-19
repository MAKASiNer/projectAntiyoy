from cell import Cell
from unit import Unit
from type import Type
from building import Building



class Player:
    def __init__(self, count=None):
        if count == None: self.count = 1
        else: self.count = count

        self.team = 1             # текущий игрок
        self.moneyPl = [0, 0, 0, 0] # деньги игроков
        # ресурсы - провизия/дерево/камень
        self.resourcesPl = [           
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    
    def decryptionTeam(self):
        if self.team == Type().redPlayer: return "красный"
        if self.team == Type().bluePlayer: return "синий"
        if self.team == Type().greenPlayer: return "зеленый"
        if self.team == Type().yellowPlayer: return "желтый"
        return "error"

    ''' меняет игрока на следующего'''
    def nextPlayer(self):
        self.team = self.team % self.count + 1
        return self.team
    
    ''' возращает текущего игрока'''
    def thisPlayer(self):
        return self.team

    ''' деньги текущего игрока '''
    def money(self, add=0):
        self.moneyPl[self.team - 1] += add
        return self.moneyPl[self.team - 1]
    
    ''' ресурсы текущего игрока '''
    def resources(self, add=[0, 0, 0]):
        self.resourcesPl[self.team - 1][0] += add[0]
        self.resourcesPl[self.team - 1][1] += add[1]
        self.resourcesPl[self.team - 1][2] += add[2]
        return self.resourcesPl[self.team - 1]