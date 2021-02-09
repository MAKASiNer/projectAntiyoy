from type import Type



''' здоровье/урон/р.перемещения/р.атаки '''
UNITPARAMETERS = [
    # void lvl  0/0/0
    [[0, 0, 0, 0]],
    # worker lvl 1
    [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1]],
    # saber lvl 1/2/3
    [[1, 1, 1, 1], [2, 2, 1, 1], [3, 3, 1, 1]],
    # assassin lvl 1/2/3
    [[0, 2, 1, 1], [1, 3, 1, 1], [2, 4, 1, 1]],
    # berserker lvl 1/2/3
    [[2, 0, 1, 1], [3, 1, 1, 1], [4, 2, 1, 1]],
    # archer lvl 1/2/3
    [[0, 1, 1, 3], [1, 2, 1, 3], [2, 3, 1, 3]],
    # caster lvl 1/2/3
    [[0, 2, 1, 2], [0, 3, 1, 2], [0, 4, 1, 2]],
    # rider lvl 1/2/3
    [[1, 1, 2, 1], [2, 2, 2, 1], [3, 3, 2, 1]],
    # lanser lvl 1/2/3
    [[1, 1, 1, 2], [2, 2, 1, 2], [3, 3, 1, 2]],
    # tower lvl 1/2/3/4
    [[1, 1, 0, 1], [2, 2, 0, 1], [3, 3, 0, 1], [4, 4, 0, 1]]
]


class Unit:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType

        if team == None: self.team = 0
        else: self.team = team


    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType: return True
        else: return False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType: return False
        else: return  True

    ''' увеличивает уровень персонажа '''
    def lvlUp(self):
        self.subType = min(self.subType + 1, len(UNITPARAMETERS[self.type]) - 1)
    
    ''' возращает здоровье персонажа '''
    def health(self):
        return UNITPARAMETERS[self.type][self.subType][0]

    ''' возращает урон персонажа '''
    def damage(self):
        return UNITPARAMETERS[self.type][self.subType][1]
    
    ''' возращает радиус перемещения персонажа '''
    def moveRange(self):
        return UNITPARAMETERS[self.type][self.subType][2]
    
    ''' возращает радиус атаки персонажа '''
    def attackRange(self):
        return UNITPARAMETERS[self.type][self.subType][3]