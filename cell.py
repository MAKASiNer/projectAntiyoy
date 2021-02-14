from type import Type



class Cell:
    def __init__(self, Type=None, subType=None, team=None):
        if Type == None: self.type = 0
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType

        if team == None: self.team = 0
        else: self.team = team

        self.isSelected = False

    def __eq__(self, other):
        if self.type == other.type and self.subType == other.subType and self.team == other.team: return True
        else: return False

    def __ne__(self, other):
        if self.type == other.type and self.subType == other.subType and self.team == other.team: return False
        else: return  True
        
    def decryptionType(self):
        if self.type == Type().void: return "вода"      
        if self.type == Type().ground:
            if self.subType == Type().forest: return "лес"        
            if self.subType == Type().mountain: return "горы"    
            if self.subType == Type().steppe: return "поле"
        return "error"
    
    def decryptionTeam(self):
        if self.team == Type().void: return "никому"
        if self.team == Type().redPlayer: return "красным"
        if self.team == Type().bluePlayer: return "синим"
        if self.team == Type().greenPlayer: return "зеленым"
        if self.team == Type().yellowPlayer: return "желтым"
        return "error"