import pygame



class Unit:
    def __init__(self, pos=None, subId=None):
        # координаты клетки юнита
        if pos == None: self.position = (0, 0)
        else: self.position = pos
