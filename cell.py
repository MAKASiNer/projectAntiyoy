class Type:
    def __init__(self):
        self.void        ='0'
        self.ground      ='1'
        self.unit        ='2'
        self.building    ='3'
        self.environment ='4'


class Cell:
    def __init__(self, Type=None, subType=None, color=None):
        if Type == None: self.type = '0'
        else: self.type = Type

        if subType == None: self.subType = 0
        else: self.subType = subType

        if color == None: self.color = (128, 128, 128)
        else: self.color = color
