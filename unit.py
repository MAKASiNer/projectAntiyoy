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
    def __init__(self, Type=None, subType=None, team=None, texture=None):
        if Type == None:
            self.type = 0
        else:
            self.type = Type

        if subType == None:
            self.subType = 0
        else:
            self.subType = subType

        if team == None:
            self.team = 0
        else:
            self.team = team

        self.move = False

    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType and self.team == other.team and self.move == other.move:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType and self.team == other.team and self.move == other.move:
            return False
        else:
            return True

    def decryptionLevel(self):
        if self.type != 0:
            return str(self.subType + 1)

    def decryptionType(self):
        if self.type == Type().worker:
            return "рабочий"
        if self.type == Type().saber:
            return "мечник"
        if self.type == Type().assassin:
            return "убийца"
        if self.type == Type().berserker:
            return "щитоносец"
        if self.type == Type().archer:
            return "лучник"
        if self.type == Type().caster:
            return "маг"
        if self.type == Type().rider:
            return "наездник"
        if self.type == Type().lancer:
            return "копейщик"
        if self.type == Type().tower:
            return "башня"
        return "error"

    def decryptionTeam(self):
        if self.team == Type().void:
            return "никому"
        if self.team == Type().redPlayer:
            return "красным"
        if self.team == Type().bluePlayer:
            return "синим"
        if self.team == Type().greenPlayer:
            return "зеленым"
        if self.team == Type().yellowPlayer:
            return "желтым"
        return "error"

    ''' увеличивает уровень персонажа '''

    def lvlUp(self, player):
        self.subType = min( self.subType + 1, len(UNITPARAMETERS[self.type]) - 1)

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
