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
        self.plates_size = (33, 33)       
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


        # отрисовка клеток поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1]))
                # селект
                if self.cell[x][y].isSelected:
                    sprite.image = self.select
                    group.add(sprite)

        # поле перемещения персонажа
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            x0 = self.selectedPos[0]
            y0 = self.selectedPos[1]

            if self.unit[x0][y0].type != Type().void:
                if self.cell[x0][y0].isSelected:
                    sprites = list()
                    # "радиус" зависит от персонажа
                    r = self.unit[x0][y0].moveRange()
                    # закрашиваем все клетки в "радиусе"
                    for _y in range(y0 - r, y0 + r + 1):
                        for _x in range(x0 - r, x0 + r + 1):
                            # если на клетке есть юнит то не закрашиваем
                            if self.unit[_x][_y].type != Type().void: continue
                            sprite = pygame.sprite.Sprite()
                            sprite.rect = (_x * self.plates_size[0], _y * self.plates_size[1])
                            # если на клетке другой персонаж, ходить нельзя 
                            sprite.image = self.freeCell

                            sprites.append(sprite)
                    group.add(sprites)

        # поле атаки персонажа
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            x0 = self.selectedPos[0]
            y0 = self.selectedPos[1]

            if self.unit[x0][y0].type != Type().void:
                if self.cell[x0][y0].isSelected:
                    sprites = list()
                    # "радиус" зависит от персонажа
                    r = self.unit[x0][y0].attackRange()
                    # закрашиваем все клетки в "радиусе"
                    for _y in range(y0 - r, y0 + r + 1):
                        for _x in range(x0 - r, x0 + r + 1):
                            # если на клетке нет юнита, то не закрашиваем
                            if x0 == _x and y0 == _y: continue
                            if self.unit[_x][_y].type == Type().void: continue
                            sprite = pygame.sprite.Sprite()
                            sprite.rect = (_x * self.plates_size[0], _y * self.plates_size[1])
                            sprite.image =  self.occupiedCell

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

                    text = '''
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    pos: {} 
                    \tcell:
                    \t\ttype:\t\t{}
                    \t\tsubType:\t{}
                    \t\tselect:\t\t{}
                    \tunit:
                    \t\ttype:\t\t{}
                    \t\tsubType:\t{}
                    \t\thealth:\t\t{}
                    \t\tdamage:\t\t{}
                    \t\tmoveRange:\t{}
                    \t\tattacRange:\t{}
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    '''.format(
                        self.selectedPos,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].type,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].subType,
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].health(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].damage(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange(),
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].attackRange())
                    print(text)

            if event.type == pygame.KEYDOWN:
                x = min(self.mousePos[0], self.size[0] - 1)
                y = min(self.mousePos[1], self.size[1] - 1)

                # спавн персонажей (временно)
                if event.key == pygame.K_0: self.unit[x][y].type, self.unit[x][y].subType = Type().worker, 0
                if event.key == pygame.K_1: self.unit[x][y].type, self.unit[x][y].subType = Type().saber, 0
                if event.key == pygame.K_2: self.unit[x][y].type, self.unit[x][y].subType = Type().assassin, 0
                if event.key == pygame.K_3: self.unit[x][y].type, self.unit[x][y].subType = Type().berserker, 0
                if event.key == pygame.K_4: self.unit[x][y].type, self.unit[x][y].subType = Type().archer, 0
                if event.key == pygame.K_5: self.unit[x][y].type, self.unit[x][y].subType = Type().caster, 0
                if event.key == pygame.K_6: self.unit[x][y].type, self.unit[x][y].subType = Type().rider, 0
                if event.key == pygame.K_7: self.unit[x][y].type, self.unit[x][y].subType = Type().lancer, 0

                # поставить/убрать визуализацию селекта на клетку
                if event.key == pygame.K_s: self.cell[x][y].isSelected = True
                if event.key == pygame.K_d: self.cell[x][y].isSelected = False

                # лвлапп персонажа
                if event.key == pygame.K_u:
                    if self.selectedPos[0] < self.size[0] and self.selectedPos[1] < self.size[1]:
                        self.unit[self.selectedPos[0]][self.selectedPos[1]].lvlUp()
                    print(self.unit[x][y].subType)
                
                # переместить
                if event.key == pygame.K_m: self.moveUnit(self.selectedPos, self.mousePos)
                # быкануть
                if event.key == pygame.K_a: self.attackUnit(self.selectedPos, self.mousePos)
    
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
    
    def attackUnit(self, From, To):
        x0, y0 = From[0], From[1]
        x1, y1 = To[0], To[1]

        if 0 <= x1 < self.size[0] and 0 <= y1 < self.size[1]:
            if self.unit[x0][y0].type != Type().void:
                # если пытаемся атаковать на слишком дальнее расстояние
                if abs(x1 - x0) > self.unit[x0][y0].attackRange() or abs(y1 - y0) > self.unit[x0][y0].attackRange(): return
                # самовыпил - не варик
                if From == To: return

                # если атакуем не пустую клетку 
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