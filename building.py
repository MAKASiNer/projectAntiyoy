from type import Type
from cell import Cell



class Building:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType

        if team == None: self.team = 0
        else: self.team = team
        
        self.move = False
    
    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType and self.team == other.team and self.move == other.move: return True
        else: return False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType and self.team == other.team and self.move == other.move: return False
        else: return  True

    def decryptionLevel(self):
        if self.type != Type().void: return str(self.subType + 1)
        
    def decryptionType(self):
        if self.type == Type().plate: return "место стройки"
        if self.type == Type().barracks: return "казармы"
        if self.type == Type().farm: return "ферма"
        if self.type == Type().quarry: return "шахта"
        if self.type == Type().sawmill: return "лесопильня"
        if self.type == Type().road: return "дорога"
        return "error"

    def decryptionTeam(self):
        if self.team == Type().void: return "никому"
        if self.team == Type().redPlayer: return "красным"
        if self.team == Type().bluePlayer: return "синим"
        if self.team == Type().greenPlayer: return "зеленым"
        if self.team == Type().yellowPlayer: return "желтым"
        return "error"
    
    ''' увеличивает уровень здания '''
    def lvlUp(self):
        self.subType = min(self.subType + 1, 2)

    ''' возращает доход со здания '''
    def revenue(self, cell=Cell()):     
        if self.type == Type().farm:
            if cell.subType == Type().steppe: return [self.subType + 1, 0, 0]
            else: return [1, 0, 0]

        if self.type == Type().sawmill:
            if cell.subType == Type().forest: return [0, self.subType + 1, 0]
            else: return [0, 1, 0]

        if self.type == Type().quarry:
            if cell.subType == Type().mountain: return [0, 0, self.subType + 1]
            else: return [0, 0, 1]
        
        return [0, 0, 0]

    ''' принимает матрицу 3х3, меняет и возращает индекс кусочка дороги (self.subType)'''
    def indexOfRoadPiece(self, mtrx):
        if mtrx == [
            [False, False, False], 
            [False, True, False], 
            [False, False, False]]: 
            self.subType = 0

        elif mtrx == [
            [False, True, False], 
            [False, True, False], 
            [False, False, False]]: 
            self.subType = 1

        elif mtrx == [
            [False, False, False], 
            [False, True, True], 
            [False, False, False]]: 
            self.subType = 2

        elif mtrx == [
            [False, False, False], 
            [False, True, False], 
            [False, True, False]]: 
            self.subType = 3

        elif mtrx == [
            [False, False, False], 
            [True, True, False], 
            [False, False, False]]: 
            self.subType = 4

        elif mtrx == [
            [False, True, False], 
            [False, True, False], 
            [False, True, False]]: 
            self.subType = 5

        elif mtrx == [
            [False, False, False], 
            [True, True, True], 
            [False, False, False]]: 
            self.subType = 6
        
        elif mtrx == [
            [False, True, False], 
            [False, True, True], 
            [False, False, False]]: 
            self.subType = 7
        
        elif mtrx == [
            [False, False, False], 
            [False, True, True], 
            [False, True, False]]: 
            self.subType = 8

        elif mtrx == [
            [False, False, False], 
            [True, True, False], 
            [False, True, False]]: 
            self.subType = 9

        elif mtrx == [
            [False, True, False], 
            [True, True, False], 
            [False, False, False]]: 
            self.subType = 10

        elif mtrx == [
            [False, True, False], 
            [False, True, True], 
            [False, True, False]]: 
            self.subType = 11

        elif mtrx == [
            [False, False, False], 
            [True, True, True], 
            [False, True, False]]: 
            self.subType = 12

        elif mtrx == [
            [False, True, False], 
            [True, True, False], 
            [False, True, False]]: 
            self.subType = 13

        elif mtrx == [
            [False, True, False], 
            [True, True, True], 
            [False, False, False]]: 
            self.subType = 14

        elif mtrx == [
            [False, True, False], 
            [True, True, True], 
            [False, True, False]]: 
            self.subType = 15

        return self.subType