class Type:
    def __init__(self):
        self.void        ='00001'
        self.ground      ='00010'
        self.unit        ='00100'
        self.building    ='01000'
        self.environment ='10000'


class Cell:
    def __init__(self, type=None, color=None):
        if type == None: self.type = Type().void
        else: self.type = type

        if color == None: self.color = (128, 128, 128)
        else: self.color = color
        
