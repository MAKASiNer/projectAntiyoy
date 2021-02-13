from PIL import Image, ImageDraw 
from cell import Cell
from unit import Unit
from type import Type
from building import Building
from player import Player
from loader import IMAGE, PLATES_SIZE
from button import Button

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
        self.stepBuffer = list()

        # размеры
        self.plates_size = PLATES_SIZE     
        # [0] - пустота, [1] - кортеж земель, [2] - кортеж юнитов, [3] - кортеж зданий, [4] - кортеж дорог, [5] - кортеж областей
        self.image = IMAGE

        # [0] - клетка занята противником, [1] - дружественным
        self.occupiedCell = [
            pygame.transform.scale(pygame.image.load("source/interface/occupiedCell0.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
            pygame.transform.scale(pygame.image.load("source/interface/occupiedCell1.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))
        ]
        self.select = pygame.transform.scale(pygame.image.load("source/interface/select.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))
        self.freeCell = pygame.transform.scale(pygame.image.load("source/interface/freeCell.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))

        # кнопки 
        self.test1 = Button(
            (((self.size[0] + 2) * self.plates_size[0], 6 * self.plates_size[1]),
            (50, 50))
        )
        self.test2 = Button(
            (((self.size[0] + 4) * self.plates_size[0], 6 * self.plates_size[1]),
            (50, 50))
        )
        self.test3 = Button(
            (((self.size[0] + 6) * self.plates_size[0], 6 * self.plates_size[1]),
            (50, 50))
        )


    def generateMapV1(self,
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

    def generateMapV2(self):
        islandCount = random.randint(2, 5)                      # количество островов
        islandLenVariation = int(self.size[0] / 2)              # модуль колебания радиусов островов
        steppeLenVariation = int(self.size[0] / 3)              # модуль колебания радиусов гор 
        mountainLenVariation = int(self.size[0] / 4)            # модуль колебания радиусов гор 
        center = (int(self.size[0] / 2), int(self.size[1] / 2)) # карты

        # изображение
        image = Image.new("RGBA", (self.size[0], self.size[1]), (255, 255, 255))
        pattern = ImageDraw.Draw(image)
        pixel = image.load()

        # центр карты - бариценр от барицентров всех островов
        # рандомно раскидываем точки, а последнюю вычисляем таким образом, чтоб бариценр от барицентров был в центре карты
        barycenterList = list()
        for _ in range(islandCount - 1):
            x0 = center[0] + random.randint(-int(self.size[0] / 4), +int(self.size[0] / 4))
            y0 = center[1] + random.randint(-int(self.size[1] / 4), +int(self.size[1] / 4) )
            barycenterList.append((x0, y0))
        x0 = center[0] * (islandCount) - sum([a[0] for a in barycenterList])
        y0 = center[0] * (islandCount) - sum([a[0] for a in barycenterList])
        barycenterList.append((x0, y0))

        # каджый барицентер - центр острова
        for barycenter in barycenterList:
            islandVertexCount = random.randint(3, 12)   # количество изломов границы острова
            steppeVertexCount = random.randint(3, 9)    # количество изломов границы степей
            mountainVertexCount = random.randint(3, 7)  # количество изломов границы гор
            vertexList = list()                 # лист вершин изломов

            # высчитываем вершины острова
            vertexList.clear()
            for angle in range(0, 360, int(360 / islandVertexCount)):
                l = random.randint(1, islandLenVariation)
                x = max(barycenter[0] + math.cos(angle * math.pi / 180) * l, 0)
                y = max(barycenter[1] + math.sin(angle * math.pi / 180) * l, 0)
                vertexList.append((min(x, self.size[0] - 1), min(y, self.size[1] - 1)))
            # рисуем остров    
            pattern.polygon(vertexList, fill=(0, 0, 0))

            # высчитываем вершины степей
            vertexList.clear()
            for angle in range(0, 360, int(360 / steppeVertexCount)):
                l = random.randint(1, steppeLenVariation)
                x = max(barycenter[0] + math.cos(angle * math.pi / 180) * l, 0)
                y = max(barycenter[1] + math.sin(angle * math.pi / 180) * l, 0)
                vertexList.append((min(x, self.size[0] - 1), min(y, self.size[1] - 1)))
            # рисуем степи   
            pattern.polygon(vertexList, fill=(50, 50, 50))
          
            # высчитываем вершины гор
            vertexList.clear()
            for angle in range(0, 360, int(360 / mountainVertexCount)):
                l = random.randint(1, mountainLenVariation)
                x = max(barycenter[0] + math.cos(angle * math.pi / 180) * l, 0)
                y = max(barycenter[1] + math.sin(angle * math.pi / 180) * l, 0)
                vertexList.append((min(x, self.size[0] - 1), min(y, self.size[1] - 1)))
            # рисуем горы         
            pattern.polygon(vertexList, fill=(100, 100, 100)) 
        
        image.save("source\pattern\pattern0.png")

        # переносим изменения на поле
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if pixel[x, y][0] == 0: self.cell[x][y] = Cell(Type().ground, Type().forest)
                if pixel[x, y][0] == 50: self.cell[x][y] = Cell(Type().ground, Type().steppe)
                if pixel[x, y][0] == 100: self.cell[x][y] = Cell(Type().ground, Type().mountain)
                elif pixel[x, y][0] == 255: self.cell[x][y] = Cell(Type().void)
        
        self.createBg()

    def createBg(self):
        image = Image.new("RGBA", (self.plates_size[0] * self.size[0], self.plates_size[1] * self.size[1]), (255, 255, 255))
        pixel = image.load()

        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                cell_l = self.cell[x][y]
                for _x in range(x * self.plates_size[0], min((x + 1) * self.plates_size[0], image.size[0])):
                    for _y in range(y * self.plates_size[1], min((y + 1) * self.plates_size[1], image.size[1])):
                        clr = self.image[cell_l.type][cell_l.subType].get_at((_x % self.plates_size[0], _y % self.plates_size[1]))
                        pixel[_x, _y] = (clr[0], clr[1], clr[2], clr[3])

        image.save("source/pattern/bg.png")
        self.background = pygame.image.load("source/pattern/bg.png")

        self.clearStepBuffer()


    def render(self, screen):
        """
        для оптимизации читать всех инитов и здания в листы, а потом из этих листов отрисовывать(а не парсить все поле)
        """
        self.renderInterface(screen)
        self.renderPlace(screen)
        self.renderArea(screen)
        self.renderSelect(screen)
        self.renderMoveRange(screen)
        self.renderAttackRange(screen)
        self.renderBuilding(screen)
        self.renderUnit(screen)

    def renderInterface(self, screen):
        # группа
        group = pygame.sprite.Group()

        # интерфейс
        screen.fill((255, 255, 255))

        #---------------------------------------------------------------------------
        # текст с инфой о клетке
        cellInfo_text = 'cell:         [type: {}, subType: {}, team: {}]'.format(
                self.cell[self.selectedPos[0]][self.selectedPos[1]].type,
                self.cell[self.selectedPos[0]][self.selectedPos[1]].subType,
                self.cell[self.selectedPos[0]][self.selectedPos[1]].team
            )

        cellInfo_font = pygame.font.Font("source/font/font1.fon", 10)
        cellInfo = cellInfo_font.render(cellInfo_text, True, (0, 0, 0))
        screen.blit(cellInfo, (
            (self.size[0] + 2) * self.plates_size[0], 
            2 * self.plates_size[1]
        ))

        # текст с инфой о юните
        unitInfo_text = 'unit:         [type: {}, subType: {}, team: {}]'.format(
                self.unit[self.selectedPos[0]][self.selectedPos[1]].type,
                self.unit[self.selectedPos[0]][self.selectedPos[1]].subType,
                self.unit[self.selectedPos[0]][self.selectedPos[1]].team
            )

        unitInfo_font = pygame.font.Font("source/font/font1.fon", 10)
        unitInfo = unitInfo_font.render(unitInfo_text, True, (0, 0, 0))
        screen.blit(unitInfo, (
            (self.size[0] + 2) * self.plates_size[0], 
            3 * self.plates_size[1]
        ))

        # текст с инфой о строение
        buildingInfo_text = 'building: [type: {}, subType: {}, team: {}]'.format(
                self.building[self.selectedPos[0]][self.selectedPos[1]].type,
                self.building[self.selectedPos[0]][self.selectedPos[1]].subType,
                self.building[self.selectedPos[0]][self.selectedPos[1]].team
            )

        buildingInfo_font = pygame.font.Font("source/font/font1.fon", 10)
        buildingInfo = buildingInfo_font.render(buildingInfo_text, True, (0, 0, 0))
        screen.blit(buildingInfo, (
            (self.size[0] + 2) * self.plates_size[0], 
            4 * self.plates_size[1]
        ))

        # текст с инфой о ресурсах
        resourcesInfo_text = 'player: [team: {}, money: {}, resuorces: {}]'.format(
                self.player.thisPlayer(),
                self.player.money(),
                self.player.resources() 
        )

        resourcesInfo_font = pygame.font.Font("source/font/font1.fon", 10)
        resourcesInfo = resourcesInfo_font.render(resourcesInfo_text, True, (0, 0, 0))
        screen.blit(resourcesInfo, (
            (self.size[0] + 2) * self.plates_size[0], 
            5 * self.plates_size[1]
        ))
        #---------------------------------------------------------------------------
        self.test1.draw(screen)
        self.test2.draw(screen)
        self.test3.draw(screen)

        if self.test1.pushDown() or self.test2.pushDown() or self.test3.pushDown(): print(1)
        if self.test1.pushUp() or self.test2.pushUp() or self.test3.pushUp(): print(0)
        # отрисовка
        group.draw(screen)

    def renderPlace(self, screen):
        # группа
        group = pygame.sprite.Group()

        # бекграунд
        sprite = pygame.sprite.Sprite()
        sprite.rect = (0, 0)
        sprite.image = self.background
        group.add(sprite)
        # отрисовка
        group.draw(screen)

    def renderArea(self, screen):
        # группа
        group = pygame.sprite.Group()
        # области игроков
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1])) 
                if self.cell[x][y].team != Type().void: 
                    sprite.image = self.image[5][self.cell[x][y].team - 1][0]
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
                sprite.rect = (int(x * self.plates_size[0]) + 1, int(y * self.plates_size[1]) + 1)
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
                            sprite = pygame.sprite.Sprite()
                            sprite.rect = (_x * self.plates_size[0] + 1, _y * self.plates_size[1] + 1)

                            try:
                                # если клетка - вода без дороги, то не красим
                                if self.cell[_x][_y].type == Type().void and self.building[_x][_y].type != Type().road: continue 

                                # если клетка - вода c дороги, то красим
                                elif self.cell[_x][_y].type == Type().void and self.building[_x][_y].type == Type().road:
                                    sprite.image = self.freeCell
                                    group.add(sprite)

                                # если на клетке есть юнит или здание то не закрашиваем
                                elif self.unit[_x][_y].type != Type().void or self.building[_x][_y].type != Type().void: continue

                                else:
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
                                sprite.rect = (_x * self.plates_size[0] + 1, _y * self.plates_size[1] + 1)

                                if self.unit[_x][_y].type != Type().void:
                                    sprite.image =  self.occupiedCell[0 if self.unit[_x][_y].team != self.unit[x0][y0].team else 1]
                                elif self.building[_x][_y].type != Type().void:
                                    sprite.image =  self.occupiedCell[0 if self.building[_x][_y].team != self.unit[x0][y0].team else 1]

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
                    sprite.image = self.image[2][self.unit[x][y].team - 1][self.unit[x][y].type - 1][self.unit[x][y].subType]
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

                # строения
                if self.building[x][y].type != Type().void and self.building[x][y].type != Type().road:
                    sprite.image = self.image[3][self.building[x][y].team - 1][self.building[x][y].type - 1][self.building[x][y].subType]
                    group.add(sprite)
                # дорога
                elif self.building[x][y].type == Type().road:
                    # матрица с ситуацией на поле 
                    piece = [[False, False, False], [False, True, False], [False, False, False]]
                    try:
                        if self.building[x][y - 1].type == Type().road: piece[0][1] = True
                        if self.building[x - 1][y].type == Type().road: piece[1][0] = True
                        if self.building[x + 1][y].type == Type().road: piece[1][2] = True
                        if self.building[x][y + 1].type == Type().road: piece[2][1] = True
                    except: pass
                    # принимаем тип дороги
                    sprite.image = self.image[4][Building().indexOfRoadPiece(piece)]
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
                    \n\t\tteam:\t\t{}\
                    \n\t\tselect:\t\t{}\
                    \n\tunit:\
                    \n\t\ttype:\t\t{}\
                    \n\t\tsubType:\t{}\
                    \n\t\tteam:\t\t{}\
                    \n\t\thealth:\t\t{}\
                    \n\t\tdamage:\t\t{}\
                    \n\t\tmoveRange:\t{}\
                    \n\t\tattacRange:\t{}\
                    \n\tbuilding:\
                    \n\t\ttype:\t\t{}\
                    \n\t\tsubType:\t{}\
                    \n\t\tteam:\t\t{}\
                    \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(
                        self.selectedPos,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].team,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].team,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].health(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].damage(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].attackRange(),
                        self.building[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.building[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.building[self.selectedPos[0]][self.selectedPos[1]].team)
                    print(text)

            if event.type == pygame.KEYDOWN:
                
                x = min(self.mousePos[0], self.size[0] - 1)
                y = min(self.mousePos[1], self.size[1] - 1)

                # спавн персонажей (временно)
                if event.key == pygame.K_0: 
                    self.unit[x][y] = Unit(Type().worker, 0, self.player.thisPlayer())
                if event.key == pygame.K_1: 
                    self.unit[x][y] = Unit(Type().saber, 0, self.player.thisPlayer())
                if event.key == pygame.K_2: 
                    self.unit[x][y] = Unit(Type().assassin, 0, self.player.thisPlayer())
                if event.key == pygame.K_3: 
                    self.unit[x][y] = Unit(Type().berserker, 0, self.player.thisPlayer())
                if event.key == pygame.K_4: 
                    self.unit[x][y] = Unit(Type().archer, 0, self.player.thisPlayer())
                if event.key == pygame.K_5: 
                    self.unit[x][y] = Unit(Type().caster, 0, self.player.thisPlayer())
                if event.key == pygame.K_6: 
                    self.unit[x][y] = Unit(Type().rider, 0, self.player.thisPlayer())
                if event.key == pygame.K_7: 
                    self.unit[x][y] = Unit(Type().lancer, 0, self.player.thisPlayer())
                if event.key == pygame.K_8: 
                    self.unit[x][y] = Unit(Type().tower, 0, self.player.thisPlayer())
                #спавн зданий (временно)
                if event.key == pygame.K_F1: 
                    self.building[x][y] = Building(Type().plate, 0, self.player.thisPlayer())
                if event.key == pygame.K_F2: 
                    self.building[x][y] = Building(Type().barracks, 0, self.player.thisPlayer())
                if event.key == pygame.K_F3: 
                    self.building[x][y] = Building(Type().farm, 0, self.player.thisPlayer())
                if event.key == pygame.K_F4: 
                    self.building[x][y] = Building(Type().quarry, 0, self.player.thisPlayer())
                if event.key == pygame.K_F5: 
                    self.building[x][y] = Building(Type().sawmill, 0, self.player.thisPlayer())
                if event.key == pygame.K_F6: 
                    self.building[x][y] = Building(Type().road, 0, self.player.thisPlayer())

                # поставить/убрать визуализацию селекта на клетку
                if event.key == pygame.K_s: self.cell[x][y].isSelected = True
                if event.key == pygame.K_d: self.cell[x][y].isSelected = False

                # лвлапп
                if event.key == pygame.K_u:
                    x = self.selectedPos[0]
                    y = self.selectedPos[1]

                    if x < self.size[0] and y < self.size[1]:
                        if self.unit[x][y].type != Type().void: self.unit[x][y].lvlUp()
                        elif self.building[x][y].type != Type().void: self.building[x][y].lvlUp()
                
                # переместить
                if event.key == pygame.K_m: self.moveUnit(self.selectedPos, self.mousePos)
                # быкануть
                if event.key == pygame.K_a: self.attackUnit(self.selectedPos, self.mousePos)

                # откат хода
                if event.key == pygame.K_z: self.loadFromStepBuffer()
                else: self.loadToStepBuffer()

                # отдать ход следующему игроку
                if event.key == pygame.K_n: 
                    print("next player: {}".format(self.player.nextPlaeyr()))
                    self.logic()
                    self.clearStepBuffer()
    
    def moveUnit(self, From, To):
        x0, y0 = From[0], From[1]
        x1, y1 = To[0], To[1]

        if 0 <= x1 < self.size[0] and 0 <= y1 < self.size[1]:
            if self.unit[x0][y0].type != Type().void:
                # если ходим на слишком далекое расстояние
                if abs(x1 - x0) > self.unit[x0][y0].moveRange() or abs(y1 - y0) > self.unit[x0][y0].moveRange(): return

                # если ходим под себя, то не ходим
                if From == To: return

                # если ходим в воду, при этом на воде нет дороги
                if self.cell[x1][y1].type == Type().void and self.building[x1][y1].type != Type().road: return

                # если ходим на пустую клетку, то ходим и занимаем клетку
                if self.unit[x1][y1].type == Type().void and (self.building[x1][y1].type == Type().void or self.building[x1][y1].type == Type().road):
                    self.unit[x0][y0], self.unit[x1][y1] = Unit(), self.unit[x0][y0]
                    self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                    self.selectedPos = (x1, y1)
                    if self.cell[x1][y1].type != Type().void: self.cell[x1][y1].team = self.unit[x1][y1].team
    
    def attackUnit(self, From, To):
        x0, y0 = From[0], From[1]
        x1, y1 = To[0], To[1]

        if 0 <= x1 < self.size[0] and 0 <= y1 < self.size[1]:
            if self.unit[x0][y0].type != Type().void:
                # если пытаемся атаковать на слишком дальнее расстояние
                if abs(x1 - x0) > self.unit[x0][y0].attackRange() or abs(y1 - y0) > self.unit[x0][y0].attackRange(): return
                # самовыпил - не варик
                if From == To: return
                # своих не бьем
                if self.unit[x0][y0].team == self.unit[x1][y1].team: return

                # если юнита
                if self.unit[x1][y1].type != Type().void:
                    # если больше атаки - то побеждаем, если атаки равны и хп больше - то побеждаем, иначе смэрть
                    win = 0
                    if self.unit[x0][y0].damage() >= self.unit[x1][y1].health(): win = True
                    elif self.unit[x0][y0].health() > self.unit[x1][y1].damage(): return
                    else: win = False

                    # милишники занимают клетку атакуемого, за искючением башен, башни - дальникик с ранжем атаки 1
                    if self.unit[x0][y0].type == Type().tower or self.unit[x0][y0].attackRange() > 1:
                        if win:
                            self.unit[x1][y1] = Unit()
                    else:
                        if win:
                            self.unit[x1][y1] = Unit()
                            self.moveUnit((x0, y0), (x1, y1))
                            self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                            self.selectedPos = (x1, y1)
                        else:
                            self.cell[x0][y0].isSelected = False
                            self.unit[x0][y0] = Unit()
                
                # если атакуем постройку
                if self.building[x1][y1].type != Type().void:
                    # милишники занимают клетку атакуемого
                    if self.unit[x0][y0].type == Type().tower or self.unit[x0][y0].attackRange() > 1:
                        self.building[x1][y1].type = Type().void 
                    else:
                        self.building[x1][y1].type = Type().void 
                        self.moveUnit((x0, y0), (x1, y1))
                        self.cell[x0][y0].isSelected, self.cell[x1][y1].isSelected = False, True
                        self.selectedPos = (x1, y1)                 

    def attackTower(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                # башни бьют всех не своих в радиусе атаки
                if self.unit[x][y].type == Type().tower:
                    # проходжим по радиусу атаки
                    r = self.unit[x][y].attackRange()
                    for _y in range(y - r, y + r + 1):
                        for _x in range(x - r, x + r + 1):
                            # башня башне башня
                            if self.unit[_x][_y].type != Type().tower:
                                self.attackUnit((x, y), (_x, _y))

    def spawnUnit(self, unit, To):
        x = To[0]
        y = To[1]
        
        # если клетка вода без дороги, то не спавним
        if self.cell[x][y].type == Type().void and self.building[x][y].type != Type().road: return 

        if self.unit[x][y].type == Type().void:
            self.unit[x][y].type = unit
            if Building[x][y].type != Type().road: Building[x][y].type = Type().road


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

    def clearStepBuffer(self):
        self.stepBuffer = [
            [
                copy.deepcopy(self.cell),
                copy.deepcopy(self.unit),
                copy.deepcopy(self.building),
                copy.deepcopy(self.selectedPos)
            ]
        ]


    def logic(self):
        self.attackTower()
        self.player.resources(add=self.calculateResources())
        self.player.money(add=self.calculateMoney())

    def calculateResources(self):
        resources = [0, 0, 0]
        # начисление ресов
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.building[x][y].team == self.player.thisPlayer():
                    if self.building[x][y].revenue():
                        add = self.building[x][y].revenue(self.cell[x][y])
                        resources = [(resources[i] + add[i]) for i in range(3)]
        return resources
    
    def calculateMoney(self):
        add = 0
        # начисление баблишка 
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.cell[x][y].team == self.player.thisPlayer():
                    add += 1
        return add
