from type import Type



class Building:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType

        if team == None: self.team = 0
        else: self.team = team
    
    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType: return True
        else: return  False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType: return False
        else: return True
    
    ''' увеличивает уровень здания '''
    def lvlUp(self):
        self.subType = min(self.subType + 1, 2)

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