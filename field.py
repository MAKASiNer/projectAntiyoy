from PIL import Image, ImageDraw 
from cell import Type, Cell
from unit import Unit

import math
import random
import pygame
import datetime



class Field:
    def __init__(self, size, playerCount, winSize):
        # игра
        self.size = size                        # размеры поля в (КЛЕТКИ по х, КЛЕТКИ по у)
        self.playerCount = playerCount          # количество игроков
        self.mousePos = (-1, -1)                # координаты мышки в клетках
        self.selectedPos = (-1, -1)             # выбранная позиция
        self.winSize = winSize                  # размеры окна

        # клетки поля
        self.cell = [[Cell() for _ in range(size[1])] for _ in range(size[0])]
        # юниты
        self.unit = [[Unit() for _ in range(size[1])] for _ in range(size[0])]

        # размеры
        self.plates_size = (25, 25)       
        # [0] - пустота, [1] - кортеж земель, [2] - кортеж юнитов, [3] - кортеж зданий, [4] - кортеж окружений   
        self.image = [
            [
                pygame.transform.scale(pygame.image.load("source/texture/void.png"), self.plates_size)
            ], 
            [
                pygame.transform.scale(pygame.image.load("source/texture/steppe.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/forest.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/mountain.png"), self.plates_size),
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/worker.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/saber.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/assassin.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/berserker.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/archer.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/caster.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/rider.png"), self.plates_size),
                pygame.transform.scale(pygame.image.load("source/texture/lancer.png"), self.plates_size)
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

        image.save("source/pattern/pattern_step_2.png")

    def render(self, screen):
        group = pygame.sprite.Group()

        # интерфейс
        sprite = pygame.sprite.Sprite()
        sprite.rect = (self.winSize[0] - (self.size[0] * self.plates_size[0]), self.winSize[1] - (self.size[1] * self.plates_size[1]))
        sprite.rect = (self.size[0] * self.plates_size[0], 0)
        sprite.image = self.lefBg
        group.add(sprite)

        '''# отрисовка селекта поля
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            selectedCell = self.cell[self.selectedPos[0]][self.selectedPos[1]]
            selectedUnit = self.unit[self.selectedPos[0]][self.selectedPos[1]]
            x0 = max(self.selectedPos[0] - selectedUnit.moveRange(), 0)
            x1 = min(self.selectedPos[0] + selectedUnit.moveRange(), self.size[0])
            y0 = min(self.selectedPos[1] + selectedUnit.moveRange(), self.size[1])
            y1 = max(self.selectedPos[1] - selectedUnit.moveRange(), 0)
            for y in range(y0, y1):
                for x in range(x0, x1):
                    self.cell[x][y].type = Type().select'''

        ''' if self.selectedPos[0] < self.size[0] and self.selectedPos[1] < self.size[1]:
            text = "sell Pos:{}\n\tsell Id:{}\t| sell subId:{}\n\tunit Id:{}\t| unit subId:{}".format(
                self.selectedPos, 
                self.cell[self.selectedPos[0]][self.selectedPos[1]].type,
                self.cell[self.selectedPos[0]][self.selectedPos[1]].subType,
                self.unit[self.selectedPos[0]][self.selectedPos[1]].type,
                self.unit[self.selectedPos[0]][self.selectedPos[1]].subType)
            print(text) '''

        # отрисовка клеток поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1]))

                # пустые клетки
                if self.cell[x][y].type == Type().void:
                    sprite.image = self.image[0][0]
                    group.add(sprite)
                
                # земля
                if self.cell[x][y].type == Type().ground:
                    sprite.image = self.image[1][self.cell[x][y].subType]
                    group.add(sprite)

                # селект
                if self.cell[x][y].isSelected:
                    sprite.image = self.select
                    group.add(sprite)

        # поле перемещения персонажа
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            if self.unit[self.selectedPos[0]][self.selectedPos[1]].type != Type().void:
                if self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected:
                    sprites = list()
                    # "радиус" зависит от персонажа
                    r = self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange()

                    # закрашиваем все клетки в "радиусе"
                    for _y in range(self.selectedPos[1] - r, self.selectedPos[1] + r + 1):
                        for _x in range(self.selectedPos[0] - r, self.selectedPos[0] + r + 1):
                            # если клетка под персонажем, то не закрашиваем
                            if _y == self.selectedPos[1] and _x == self.selectedPos[0]: continue
                            sprite = pygame.sprite.Sprite()
                            sprite.rect = (_x * self.plates_size[0], _y * self.plates_size[1])
                            # если на клетке другой персонаж, ходить нельзя 
                            if self.unit[_x][_y].type == Type().void: sprite.image = self.freeCell
                            else:sprite.image =  self.occupiedCell

                            sprites.append(sprite)
                    group.add(sprites)
                
        # отрисовка окружения поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1])) 

                # юниты
                if self.unit[x][y].type != Type().void:
                    sprite.image = self.image[2][self.unit[x][y].type - 1]
                    group.add(sprite)

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

                    text = "sell Pos:{}\n\tsell Id:{}\t| sell subId:{}\n\tunit Id:{}\t| unit subId:{}".format(
                        self.selectedPos, 
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].subType)
                    print(text)

            if event.type == pygame.KEYDOWN:
                x = min(self.mousePos[0], self.size[0] - 1)
                y = min(self.mousePos[1], self.size[1] - 1)

                # спавн персонажей (временно)
                if event.key == pygame.K_0: self.unit[x][y].type = Type().worker
                if event.key == pygame.K_1: self.unit[x][y].type = Type().saber
                if event.key == pygame.K_2: self.unit[x][y].type = Type().assassin
                if event.key == pygame.K_3: self.unit[x][y].type = Type().berserker
                if event.key == pygame.K_4: self.unit[x][y].type = Type().archer
                if event.key == pygame.K_5: self.unit[x][y].type = Type().caster
                if event.key == pygame.K_6: self.unit[x][y].type = Type().rider
                if event.key == pygame.K_7: self.unit[x][y].type = Type().lancer

                # поставить/убрать визуализацию селекта на клетку
                if event.key == pygame.K_s: self.cell[x][y].isSelected = True
                if event.key == pygame.K_d: self.cell[x][y].isSelected = False

                # лвлапп персонажа
                if event.key == pygame.K_u:
                    if self.selectedPos[0] < self.size[0] and self.selectedPos[1] < self.size[1]:
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].lvlUp()
                    print(self.unit[x][y].subType)
                
                # перемещение
                if event.key == pygame.K_m:
                    self.moveUnit(self.selectedPos, self.mousePos)
                    '''if self.selectedPos[0] < self.size[0] and self.selectedPos[1] < self.size[1]:
                        if self.unit[self.selectedPos[0]][self.selectedPos[1]].type != Type().void:
                            # если ходим не под себя
                            if self.selectedPos != self.mousePos:
                                # если ходим на заданное расстояние
                                if abs(self.selectedPos[0] - self.mousePos[0]) <= self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange() and \
                                   abs(self.selectedPos[1] - self.mousePos[1]) <= self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange():
                                    # переносим персонажа
                                    self.unit[self.mousePos[0]][self.mousePos[1]] = self.unit[self.selectedPos[0]][self.selectedPos[1]]
                                    self.unit[self.selectedPos[0]][self.selectedPos[1]] = Unit()
                                    # переносим селект
                                    self.cell[self.mousePos[0]][self.mousePos[1]].isSelected = True
                                    self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected = False
                                    self.selectedPos = (x, y)'''
    
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
                if self.unit[x1][y1].type == Type().void:
                    self.unit[x0][y0], self.unit[x1][y1] = Unit(), self.unit[x0][y0]
                    self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                    self.selectedPos = (x1, y1)
    
                # если клетка не пуста, то ходим только в том случае, если униту хватает атаки
                else:
                    if self.unit[x0][y0].damage() >= self.unit[x1][y1].health():
                        self.unit[x0][y0], self.unit[x1][y1] = Unit(), self.unit[x0][y0]
                        self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                        self.selectedPos = (x1, y1)