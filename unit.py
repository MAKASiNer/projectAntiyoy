from type import Type



# hp/dmg/mr/ar
UNITPARAMETERS = [
    # void
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
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
    [[1, 1, 1, 2], [2, 2, 1, 2], [3, 3, 1, 2]]
]


class Unit:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType

    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType: return True
        else: return False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType: return False
        else: return  True

    def lvlUp(self):
        self.subType = min(self.subType + 1, 2)
    
    def health(self):
        return UNITPARAMETERS[self.type][self.subType][0]

    def damage(self):
        return UNITPARAMETERS[self.type][self.subType][1]
    
    def moveRange(self):
        return UNITPARAMETERS[self.type][self.subType][2]
    
    def attackRange(self):
        return UNITPARAMETERS[self.type][self.subType][3]


'''
{имя} - уровней {количество} : {здоровье, урон, дальность передвижения, дальность атаки} : {доп свойства}


worker - уровней - 1 : (0 0 2 1) : улучшается в любого, обьединяется с любым

saber - уровней - 3 : (1 1 2 1) (2 2 2 1) (3 3 2 1) 
assassin - уровней - 3 : (0 2 2 1) (1 3 2 1) (2 4 2 1) : содержание + / здоровье - / урон +
berserker - уровней - 3 : (2 0 2 1) (3 1 2 1) (4 2 2 1) : содержание + / здоровье + / урон -
archer - уровней - 3 : (0 1 2 3) (1 2 2 3) (2 3 2 3) : содержание ++ / дальность атаки ++ / здоровье -
caster - уровней - 3 : (0 2 2 2) (0 3 2 2) (0 4 2 2) : дальность атаки + / содержание + / здоровье - / урон +
rider - уровней - 3: (1 1 3 1) (2 2 3 1) (3 3 3 1) : дальность передвижения + / содержание ++ / проходит через юнитов
lancer - уровней - 3: (1 1 2 2) (2 2 2 2) (3 3 2 2) : дальность атаки + / содержание ++ / здоровье - 


передвижение по воде в 2 раза ниже

после убийства archer, caster и lancer не захватывают клетку под убитым 

worker получает больше ресурсов при добыче


'''