from PIL import Image, ImageDraw 
from cell import Cell
from unit import Unit
from type import Type
from building import Building
from player import Player

import copy
import math
import random
import pygame
import datetime



class Game:
    def __init__(self, size, playerCount, winSize):
        # игра
        self.size = size                        # размеры поля в (КЛЕТКИ по х, КЛЕТКИ по у)
        self.player = Player(playerCount)       # игроки
        self.mousePos = (-1, -1)                # координаты мышки в клетках
        self.selectedPos = (-1, -1)             # выбранная позиция
        self.winSize = winSize                  # размеры окна          

        # клетки поля
        self.cell = [[Cell() for _ in range(size[1])] for _ in range(size[0])]
        # юниты
        self.unit = [[Unit() for _ in range(size[1])] for _ in range(size[0])]
        # постройки
        self.building = [[Building() for _ in range(size[1])] for _ in range(size[0])]

        # буффер ходов
        self.stepBuffer = [
            [
                copy.deepcopy(self.cell),
                copy.deepcopy(self.unit),
                copy.deepcopy(self.building),
                copy.deepcopy(self.selectedPos)
            ]
        ]

        # размеры
        self.plates_size = (33, 33)       
        # [0] - пустота, [1] - кортеж земель, [2] - кортеж юнитов, [3] - кортеж зданий, [4] - кортеж дорог
        self.image = [
            # 0
            [
                pygame.transform.scale(pygame.image.load("source/texture/void.png"), self.plates_size)
            ], 
            # 1
            [
                pygame.transform.scale(pygame.image.load("source/texture/ground/steppe.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/ground/forest.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/ground/mountain.png"), self.plates_size),
            ],
            # 2
            [
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/worker0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/worker1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/worker2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/saber0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/saber1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/saber2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/assassin0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/assassin1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/assassin2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/berserker0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/berserker1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/berserker2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/archer0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/archer1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/archer2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/caster0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/caster1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/caster2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/rider0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/rider1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/rider2.png"), self.plates_size)
                ],
                [
                    pygame.transform.scale(pygame.image.load("source/texture/unit/lancer0.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/lancer1.png"), self.plates_size),
                    pygame.transform.scale(pygame.image.load("source/texture/unit/lancer2.png"), self.plates_size)
                ]
            ],
            # 3
            [
                pygame.transform.scale(pygame.image.load("source/texture/building/plate.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/barracks.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/farm.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/quarry.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/sawmill.png"), self.plates_size)
            ],
            # 4
            [
                pygame.transform.scale(pygame.image.load("source/texture/building/road0.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road1.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road2.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road3.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road4.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road5.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road6.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road7.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road8.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road9.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road10.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road11.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road12.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road13.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road14.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/building/road15.png"), self.plates_size)
            ]
        ]

        # интерфейс
        self.select = pygame.transform.scale(pygame.image.load("source/interface/select.png"), self.plates_size)
        self.occupiedCell = pygame.transform.scale(pygame.image.load("source/interface/occupiedCell.png"), self.plates_size)
        self.freeCell = pygame.transform.scale(pygame.image.load("source/interface/freeCell.png"), self.plates_size)
        self.lefBg = pygame.transform.scale(pygame.image.load("source/interface/left_bg.png"), (300, 1000))


    def generateMap(self, 
        seed=None, 
        peakCount=None, 
        peakRadius=None, 
        peakVerticesRange=None, 
        peakVerticesCount=None,
        holeCount=None, 
        holeRadius=None, 
        holeVerticesRange=None, 
        holeVerticesCount=None,
        steppePercentage=None,
        forestPercentage=None,
        mountainPercentage=None
        ):
        '''
        seed: int - сид генерации\n
        peakCount: int - количество опорных точек пиков\n
        peakRadius: (int, int) - диапазон радиусов опорных точек пиков\n
        peakVerticesRange: (int, int) - диапазон колебаний длин направлений пиков\n
        peakVerticesCount: (int, int) - количество направлений пиков\n
        holeCount: int - количество опорных точек дырок\n
        holeRadius: (int, int) - диапазон радиусов опорных точек дырок\n
        holeVerticesRange: (int, int) - диапазон колебаний длин направлений дырок\n
        holeVerticesCount: (int, int) - количество направлений дырок\n
        steppePercentage: float - концентрация степей
        forestPercentage: float - концентрация лесов\n
        mountainPercentage: float - концентрация гор\n
        '''

        # сид генерации
        if seed == None: self.seed = datetime.datetime.now().microsecond
        else: self.seed = seed
        random.seed = self.seed

        # количество опорных точек пиков
        if peakCount == None: self.peakCount = random.randint(2, 7)
        else: self.peakCount = peakCount

        # диапазон радиусов опорных точек пиков
        if peakRadius == None: self.peakRadius = (100, 500)
        else: self.peakRadius = peakRadius

        # диапазон колебаний длин направлений пиков
        if peakVerticesRange == None: self.peakVerticesRange = (-100, +500)
        else: self.peakVerticesRange = peakVerticesRange

        # количество направлений пиков
        if peakVerticesCount == None: self.peakVerticesCount = random.randint(3, 10)
        else: self.peakVerticesCount = random.randint(peakVerticesCount[0], peakVerticesCount[1])

        # количество опорных точек дырок
        if holeCount == None: self.holeCount = random.randint(0, 30)
        else: self.holeCount = holeCount

        # диапазон радиусов опорных точек дырок
        if holeRadius == None: self.holeRadius = (-100, 500)
        else: self.holeRadius = holeRadius

        # диапазон колебаний длин направлений дырок
        if holeVerticesRange == None: self.holeVerticesRange = (-50, +300)
        else: self.holeVerticesRange = holeVerticesRange

        # количество направлений дырок
        if holeVerticesCount == None: self.holeVerticesCount = random.randint(3, 15)
        else: self.holeVerticesCount = random.randint(holeVerticesCount[0], holeVerticesCount[1])

        # концентрация степей
        if steppePercentage == None: self.steppePercentage = 0.8
        else: self.steppePercentage = steppePercentage

        # концентрация лесов
        if forestPercentage == None: self.forestPercentage = 0.2
        else: self.forestPercentage = forestPercentage
        
        # концентрация гор
        if mountainPercentage == None: self.mountainPercentage = 0.9
        else: self.mountainPercentage = mountainPercentage

        # первым делом создается изображение
        image = Image.new("RGBA", (2000, 2000), (255, 255, 255))
        pattern = ImageDraw.Draw(image)
        pixel = image.load()

        # порные точки пиков
        peak = [(random.randint(image.size[0] / 2 + self.peakVerticesRange[0], image.size[1] / 2 + self.peakVerticesRange[1]), 
                random.randint(image.size[0] / 2 + self.peakVerticesRange[0], image.size[1] / 2 + self.peakVerticesRange[1])) 
                for _ in range(self.peakCount)]

        # от каждой опорной точки пиков откладывается направления на расстояние радиус + колебание радиуса 
        for center in peak:
            length = random.randint(self.peakRadius[0], self.peakRadius[1])
            coord = list()
            for angle in range(0, 360, int(360 / self.peakVerticesCount)):
                len_l = length + random.randint(self.peakVerticesRange[0], self.peakVerticesRange[1])
                x = center[0] + math.cos(angle * math.pi / 180) * len_l
                y = center[1] + math.sin(angle * math.pi / 180) * len_l
                coord.append((x, y))
            pattern.polygon(coord, fill=(0, 0, 0))

        # опорные точки дырок
        hole = [(random.randint(0, image.size[0]), random.randint(0, image.size[1])) for _ in range(self.holeCount)]

        # от каждой опорной точки дырок откладывается направления на расстояние радиус + колебание радиуса 
        for center in hole:
            length = random.randint(self.holeRadius[0], self.holeRadius[1])
            coord = list()
            for angle in range(0, 360, int(360 / self.holeVerticesCount)):
                len_l = length + random.randint(self.holeVerticesRange[0], self.holeVerticesRange[1])
                x = center[0] + math.cos(angle * math.pi / 180) * len_l
                y = center[1] + math.sin(angle * math.pi / 180) * len_l
                coord.append((x, y))

            # выбор типа заполнения дырки
            a = (float(random.randint(0, 100)) / 100)
            b = (float(random.randint(0, 100)) / 100)
            c = (float(random.randint(0, 100)) / 100)

            if a < self.forestPercentage: clr = (50, 50, 50)
            elif b < self.steppePercentage: clr = (100, 100, 100)
            elif c < self.mountainPercentage: clr = (150, 150, 150)
            else: clr = (255, 255, 255)

            
            pattern.polygon(coord, fill=clr)

        image.save("source/pattern/pattern_step_1.png")

        # делим изображение сеткой, и закрашиваем
        for x in range(0, image.size[0], int(image.size[0] / self.size[0])):
            for y in range(0, image.size[1], int(image.size[1] / self.size[1])):
                clr = 0
                whitePxl = False
                for _x in range(x, min(x + int(image.size[0] / self.size[0]), image.size[0])):
                    for _y in range(y, min(y + int(image.size[1] / self.size[1]), image.size[1])):
                        if not whitePxl and (pixel[_x, _y])[0] == 255: whitePxl = True
                        clr += (pixel[_x, _y])[0]
                
                pxlCount = (min(x + int(image.size[0] / self.size[0]), image.size[0]) - x) * (min(y + int(image.size[1] / self.size[1]), image.size[1]) - y)
                if whitePxl: clr = 255
                else: clr /= pxlCount

                if clr <= 50: clr = (50, 50, 50)
                elif clr <= 100: clr = (100, 100, 100)
                elif clr <= 150: clr = (150, 150, 150)
                else: clr = (255, 255, 255)

                for _x in range(x, min(x + int(image.size[0] / self.size[0]), image.size[0])):
                    for _y in range(y, min(y + int(image.size[1] / self.size[1]), image.size[0])):
                        pixel[_x, _y] = clr
                
                if clr == (50, 50, 50): self.cell[int(x * self.size[0] / 2000)][int(y * self.size[1] / 2000)] = Cell(Type().ground, 1)
                elif clr == (100, 100, 100): self.cell[int(x * self.size[0] / 2000)][int(y * self.size[1] / 2000)] = Cell(Type().ground, 2)
                elif clr == (150, 150, 150): self.cell[int(x * self.size[0] / 2000)][int(y * self.size[1] / 2000)] = Cell(Type().ground, 0)
                elif clr == (255, 255, 255): self.cell[int(x * self.size[0] / 2000)][int(y * self.size[1] / 2000)] = Cell(Type().void)

        # создаем бекграунд
        image.save("source/pattern/pattern_step_2.png")
        image = Image.new("RGBA", (self.plates_size[0] * self.size[0] - 1, self.plates_size[1] * self.size[1] - 1), (255, 255, 255))
        pixel = image.load()

        for x in range(0, image.size[0]):
            for y in range(0, image.size[1]):

                _x = x // self.plates_size[0]
                _y = y // self.plates_size[1]
                cell_l = self.cell[_x][_y]

                if cell_l.type == Type().void or cell_l.type == Type().ground:
                    clr = self.image[cell_l.type][cell_l.subType].get_at((x % self.plates_size[0], y % self.plates_size[1 ]))
                    pixel[x, y] = (clr[0], clr[1], clr[2], clr[3])
        image.save("source/pattern/pattern_step_3.png")
        self.background = pygame.image.load("source/pattern/pattern_step_3.png")

    def render(self, screen):
        self.renderPlace(screen)
        self.renderSelect(screen)
        self.renderMoveRange(screen)
        self.renderAttackRange(screen)
        self.renderUnit(screen)
        self.renderBuilding(screen)

    def renderPlace(self, screen):
        # группа
        group = pygame.sprite.Group()
        # интерфейс
        sprite = pygame.sprite.Sprite()
        sprite.rect = (self.winSize[0] - (self.size[0] * self.plates_size[0]), self.winSize[1] - (self.size[1] * self.plates_size[1]))
        sprite.rect = (self.size[0] * self.plates_size[0], 0)
        sprite.image = self.lefBg
        group.add(sprite)
        # бекграунд
        sprite = pygame.sprite.Sprite()
        sprite.rect = (0, 0)
        sprite.image = self.background
        group.add(sprite)
        # отрисовка
        group.draw(screen)

    def renderSelect(self, screen):
        # группа
        group = pygame.sprite.Group()
        # отрисовка селекта
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1]))
                # селект
                if self.cell[x][y].isSelected:
                    sprite.image = self.select
                    group.add(sprite)
        # отрисовка
        group.draw(screen)

    def renderMoveRange(self, screen):
        # группа
        group = pygame.sprite.Group()
        # поле перемещения персонажа
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            x0 = self.selectedPos[0]
            y0 = self.selectedPos[1]
            if self.unit[x0][y0].type != Type().void:
                if self.cell[x0][y0].isSelected:
                    # "радиус" зависит от персонажа
                    r = self.unit[x0][y0].moveRange()
                    # закрашиваем все клетки в "радиусе"
                    for _y in range(y0 - r, y0 + r + 1):
                        for _x in range(x0 - r, x0 + r + 1):
                            # если на клетке есть юнит или здание то не закрашиваем
                            try:
                                if self.unit[_x][_y].type != Type().void or self.building[_x][_y].type != Type().void: continue
                                sprite = pygame.sprite.Sprite()
                                sprite.rect = (_x * self.plates_size[0], _y * self.plates_size[1])
                                # если на клетке другой персонаж, ходить нельзя 
                                sprite.image = self.freeCell
                                group.add(sprite)
                            except: pass
        # отрисовка
        group.draw(screen)

    def renderAttackRange(self, screen):
        # группа
        group = pygame.sprite.Group()
        # поле атаки персонажа
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            x0 = self.selectedPos[0]
            y0 = self.selectedPos[1]
            if self.unit[x0][y0].type != Type().void:
                if self.cell[x0][y0].isSelected:
                    # "радиус" зависит от персонажа
                    r = self.unit[x0][y0].attackRange()
                    # закрашиваем все клетки в "радиусе"
                    for _y in range(y0 - r, y0 + r + 1):
                        for _x in range(x0 - r, x0 + r + 1):
                            # если на клетке нет ни юнита, ни здания, то не закрашиваем
                            if x0 == _x and y0 == _y: continue
                            try:
                                if self.unit[_x][_y].type == Type().void and self.building[_x][_y].type == Type().void: continue
                                sprite = pygame.sprite.Sprite()
                                sprite.rect = (_x * self.plates_size[0], _y * self.plates_size[1])
                                sprite.image =  self.occupiedCell
                                group.add(sprite)
                            except: pass
        # отрисовка
        group.draw(screen)

    def renderUnit(self, screen):
        # группа
        group = pygame.sprite.Group()
        # отрисовка окружения поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1]))
                # юниты
                if self.unit[x][y].type != Type().void:
                    sprite.image = self.image[2][self.unit[x][y].type - 1][self.unit[x][y].subType]
                    group.add(sprite)
        # отрисовка
        group.draw(screen)

    def renderBuilding(self, screen):
        # группа
        group = pygame.sprite.Group()
        # отрисовка окружения поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1])) 
                # здания
                if self.building[x][y].type != Type().void:
                    sprite.image = self.image[3][self.building[x][y].type - 1]
                    group.add(sprite)
        # отрисовка
        group.draw(screen)


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # задаем координаты мышки
            if event.type == pygame.MOUSEMOTION:
                x = event.pos[0] // self.plates_size[0]
                y = event.pos[1] // self.plates_size[1]
                self.mousePos = (x, y)

            # задаем селект
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    x = min(self.mousePos[0], self.size[0] - 1)
                    y = min(self.mousePos[1], self.size[1] - 1)
                    self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected = False
                    self.cell[x][y].isSelected = True
                    self.selectedPos = (x, y)

                    text = "\
                    \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
                    \npos: {}\
                    \n\tcell:\
                    \n\t\ttype:\t\t{}\
                    \n\t\tsubType:\t{}\
                    \n\t\tselect:\t\t{}\
                    \n\tunit:\
                    \n\t\ttype:\t\t{}\
                    \n\t\tsubType:\t{}\
                    \n\t\thealth:\t\t{}\
                    \n\t\tdamage:\t\t{}\
                    \n\t\tmoveRange:\t{}\
                    \n\t\tattacRange:\t{}\
                    \n\tbuilding:\
                    \n\t\ttype:\t\t{}\
                    \n\t\tsubType:\t{}\
                    \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(
                        self.selectedPos,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].health(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].damage(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].attackRange(),
                        self.building[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.building[self.selectedPos[0]][self.selectedPos[1]].subType)
                    print(text)

            if event.type == pygame.KEYDOWN:
                
                x = min(self.mousePos[0], self.size[0] - 1)
                y = min(self.mousePos[1], self.size[1] - 1)

                # спавн персонажей (временно)
                if event.key == pygame.K_0: 
                    self.unit[x][y] = Unit(Type().worker)
                if event.key == pygame.K_1: 
                    self.unit[x][y] = Unit(Type().saber)
                if event.key == pygame.K_2: 
                    self.unit[x][y] = Unit(Type().assassin)
                if event.key == pygame.K_3: 
                    self.unit[x][y] = Unit(Type().berserker)
                if event.key == pygame.K_4: 
                    self.unit[x][y] = Unit(Type().archer)
                if event.key == pygame.K_5: 
                    self.unit[x][y] = Unit(Type().caster)
                if event.key == pygame.K_6: 
                    self.unit[x][y] = Unit(Type().rider)
                if event.key == pygame.K_7: 
                    self.unit[x][y] = Unit(Type().lancer)
                #спавн зданий (временно)
                if event.key == pygame.K_F1: self.building[x][y].type, self.building[x][y].subType = Type().plate, 0
                if event.key == pygame.K_F2: self.building[x][y].type, self.building[x][y].subType = Type().barracks, 0
                if event.key == pygame.K_F3: self.building[x][y].type, self.building[x][y].subType = Type().farm, 0
                if event.key == pygame.K_F4: self.building[x][y].type, self.building[x][y].subType = Type().quarry, 0
                if event.key == pygame.K_F5: self.building[x][y].type, self.building[x][y].subType = Type().sawmill, 0
                # юниты уничтожают здания (временно)
                if self.unit[x][y].type != Type().void: self.building[x][y] = Building()

                # поставить/убрать визуализацию селекта на клетку
                if event.key == pygame.K_s: self.cell[x][y].isSelected = True
                if event.key == pygame.K_d: self.cell[x][y].isSelected = False

                # лвлапп
                if event.key == pygame.K_u:
                    if self.selectedPos[0] < self.size[0] and self.selectedPos[1] < self.size[1]:
                        if self.unit[x][y].type != Type().void: self.unit[self.selectedPos[0]][self.selectedPos[1]].lvlUp()
                        if self.building[x][y].type != Type().void: self.building[self.selectedPos[0]][self.selectedPos[1]].lvlUp()
                
                # переместить
                if event.key == pygame.K_m: self.moveUnit(self.selectedPos, self.mousePos)
                # быкануть
                if event.key == pygame.K_a: self.attackUnit(self.selectedPos, self.mousePos)

                # откат хода
                if event.key == pygame.K_z: self.loadFromStepBuffer()
                else: self.loadToStepBuffer()

                # отдать ход следующему игроку
                if event.key == pygame.K_n: print("next player: {}".format(self.player.nextPlaeyr()))
    
    def moveUnit(self, From, To):
        x0, y0 = From[0], From[1]
        x1, y1 = To[0], To[1]

        if 0 <= x1 < self.size[0] and 0 <= y1 < self.size[1]:
            if self.unit[x0][y0].type != Type().void:
                # если ходим на слишком далекое расстояние
                if abs(x1 - x0) > self.unit[x0][y0].moveRange() or abs(y1 - y0) > self.unit[x0][y0].moveRange(): return

                # если ходим под себя, то не ходим
                if From == To: return

                # если ходим на пустую клетку, то ходим
                if self.unit[x1][y1].type == Type().void and self.building[x1][y1].type == Type().void:
                    self.unit[x0][y0], self.unit[x1][y1] = Unit(), self.unit[x0][y0]
                    self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                    self.selectedPos = (x1, y1)
    
    def attackUnit(self, From, To):
        x0, y0 = From[0], From[1]
        x1, y1 = To[0], To[1]

        if 0 <= x1 < self.size[0] and 0 <= y1 < self.size[1]:
            if self.unit[x0][y0].type != Type().void:
                # если пытаемся атаковать на слишком дальнее расстояние
                if abs(x1 - x0) > self.unit[x0][y0].attackRange() or abs(y1 - y0) > self.unit[x0][y0].attackRange(): return
                # самовыпил - не варик
                if From == To: return

                # если юнита
                if self.unit[x1][y1].type != Type().void:
                    
                    # если больше атаки - то побеждаем, если атаки равны и хп больше - то побеждаем, иначе смэрть
                    win = 0
                    if self.unit[x0][y0].damage() >= self.unit[x1][y1].health(): win = True
                    elif self.unit[x0][y0].health() > self.unit[x1][y1].damage(): return
                    else: win = False

                    # милишники занимают клетку атакуемого
                    if self.unit[x0][y0].attackRange() == 1:
                        if win:
                            self.unit[x0][y0], self.unit[x1][y1] = Unit(), self.unit[x0][y0]
                            self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                            self.selectedPos = (x1, y1)
                        else:
                            self.cell[x0][y0].isSelected = False
                            self.unit[x0][y0] = Unit()

                    # дальники просто убивают
                    else:
                        if win:
                            self.unit[x1][y1] = Unit()
                
                # если атакуем постройку
                if self.building[x1][y1].type != Type().void:
                    # милишники занимают клетку атакуемого
                    if self.unit[x0][y0].attackRange() == 1:
                            self.unit[x0][y0], self.unit[x1][y1] = Unit(), self.unit[x0][y0]
                            self.building[x1][y1].type = Type().void if self.building[x1][y1].type == Type().plate else Type().plate
                            self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                            self.selectedPos = (x1, y1)
                    # дальники просто убивают
                    else:
                        self.building[x1][y1].type = Type().void if self.building[x1][y1].type == Type().plate else Type().plate

    def loadToStepBuffer(self):
        # елемент содержит информацию о клетках, юнитах, строениях и селекту
        element = [
            copy.deepcopy(self.cell),
            copy.deepcopy(self.unit),
            copy.deepcopy(self.building),
            copy.deepcopy(self.selectedPos)
        ]

        # проверка, отличается ли новый элемент от предыдущего
        state = False

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if element[0][x][y] != self.stepBuffer[-1][0][x][y]: state = True
                elif element[1][x][y] != self.stepBuffer[-1][1][x][y]: state = True
                elif element[2][x][y] != self.stepBuffer[-1][2][x][y]: state = True
                if state: break
            if state: break

        # если отличается, заливает в буффер
        if state: self.stepBuffer.append(element)     
            
    def loadFromStepBuffer(self):
        # если в буффере более 1 элемента
        indx = len(self.stepBuffer) - 2

        if indx > 0:
            # вытаскивает предпоследний элемент буффера
            element = self.stepBuffer.pop(indx)
            self.cell = element[0]
            self.unit = element[1]
            self.building = element[2]
            self.selectedPos = element[3]
        else:
            # еее кастылина (удаляет последний элемент)
            if len(self.stepBuffer) > 1: self.stepBuffer.pop()
            
            # копирует первый элемент буфера
            element = copy.deepcopy(self.stepBuffer[0])
            self.cell = element[0]
            self.unit = element[1]
            self.building = element[2]
            self.selectedPos = element[3]
