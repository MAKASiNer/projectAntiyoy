'''
Основные Id(type) обьектов

По умолчанию у всех обьектов стоит тип void = пустой

Нумерация типов начинается с 1 т.к. для всех по умолчанию стоит void == 0
'''


class Type:
    def __init__(self):
        self.void        =0

        self.ground      =1
        self.unit        =2
        self.building    =3
        self.environment =4
        self.select      =5

        self.worker      =1
        self.saber       =2
        self.assassin    =3
        self.berserker   =4
        self.archer      =5
        self.caster      =6
        self.rider       =7
        self.lancer      =8

        self.barracks    =1
        self.farm        =2
        self.quarry      =3
        self.sawmillё    =4