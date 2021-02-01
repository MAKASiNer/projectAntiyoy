from type import Type



class Building:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType
    
    def lvlUp(self):
        self.subType = min(self.subType + 1, 2)