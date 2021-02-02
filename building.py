from type import Type



class Building:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType
    
    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType: return True
        else: return  False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType: return False
        else: return True
    
    def lvlUp(self):
        self.subType = min(self.subType + 1, 2)