from PIL import Image, ImageDraw 
from cell import Cell
from unit import Unit
from type import Type
from building import Building
from player import Player
from loader import IMAGE, PLATES_SIZE

import copy
import math
import random
import pygame



class Game:
    def __init__(self, size, playerCount, winSize):
        # игра
        self.size = size                        # размеры поля в (КЛЕТКИ по х, КЛЕТКИ по у)
        self.player = Player(playerCount)       # игроки
        self.mousePos = (-1, -1)                # координаты мышки в клетках
        self.selectedPos = (0, 0)               # выбранная позиция
        self.winSize = winSize                  # размеры окна
        self.sideShift = 400                    # сдвиг от левого бока   

        
        self.cell = [[Cell() for _ in range(size[1])] for _ in range(size[0])]          # клетки поля      
        self.unit = [[Unit() for _ in range(size[1])] for _ in range(size[0])]          # юниты      
        self.building = [[Building() for _ in range(size[1])] for _ in range(size[0])]  # постройки

        # буффер ходов
        self.stepBuffer = list()

        # размеры плитки
        self.plates_size = PLATES_SIZE    
         
        # подгрузка текстур
        self.imageVoid = IMAGE[0]
        self.imageGround = IMAGE[1]
        self.imageUnit = list()
        self.imageBuilding = list()
        self.imageRoad = IMAGE[4]
        self.imageArea = list()
        
        # раздутие текстур для персонажей
        for ref in IMAGE[2]:
            pl1 = ref.copy()
            pl2 = ref.copy()
            pl3 = ref.copy()
            pl4 = ref.copy()
            
            pl1.fill((255, 30, 30), special_flags=pygame.BLEND_MIN)
            pl2.fill((30, 255, 255), special_flags=pygame.BLEND_MIN)
            pl3.fill((30, 255, 30), special_flags=pygame.BLEND_MIN)
            pl4.fill((255, 255, 30), special_flags=pygame.BLEND_MIN)
            self.imageUnit.append([pl1, pl2, pl3, pl4])
            
        # раздутие текстур для зданий
        for ref in IMAGE[3]:
            pl1 = ref.copy()
            pl2 = ref.copy()
            pl3 = ref.copy()
            pl4 = ref.copy()
            
            pl1.fill((255, 30, 30), special_flags=pygame.BLEND_MIN)
            pl2.fill((30, 255, 255), special_flags=pygame.BLEND_MIN)
            pl3.fill((30, 255, 30), special_flags=pygame.BLEND_MIN)
            pl4.fill((255, 255, 30), special_flags=pygame.BLEND_MIN)
            self.imageBuilding.append([pl1, pl2, pl3, pl4])
            
        # раздутие текстур для площадей
        for ref in IMAGE[5]:
            pl1 = ref.copy()
            pl2 = ref.copy()
            pl3 = ref.copy()
            pl4 = ref.copy()
            
            pl1.fill((255, 30, 30), special_flags=pygame.BLEND_MULT)
            pl2.fill((30, 255, 255), special_flags=pygame.BLEND_MIN)
            pl3.fill((30, 255, 30), special_flags=pygame.BLEND_MIN)
            pl4.fill((255, 255, 30), special_flags=pygame.BLEND_MIN)
            self.imageArea.append([pl1, pl2, pl3, pl4])

        # [0] - клетка занята противником, [1] - дружественным
        self.occupiedCell = [
            pygame.transform.scale(pygame.image.load("source/interface/occupiedCell0.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
            pygame.transform.scale(pygame.image.load("source/interface/occupiedCell1.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))
        ]
        self.select = pygame.transform.scale(pygame.image.load("source/interface/select.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))
        self.freeCell = pygame.transform.scale(pygame.image.load("source/interface/freeCell.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))
        
        # изображения уровней
        self.levelImage = [
            pygame.transform.scale(pygame.image.load("source/texture/unit/lvl1.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
            pygame.transform.scale(pygame.image.load("source/texture/unit/lvl2.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
            pygame.transform.scale(pygame.image.load("source/texture/unit/lvl3.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
            pygame.transform.scale(pygame.image.load("source/texture/unit/lvl4.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
        ]
        
        # тень
        self.shadowImage = pygame.transform.scale(pygame.image.load("source/texture/unit/shadow.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))


    def generateMap(self):
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
        image.save("source\pattern\pattern.png")
        
        self.createBg()

    def createBg(self):
        image = Image.open("source\pattern\pattern.png")
        pixel = image.load()
        
        # переносим изменения на поле
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if pixel[x, y][0] == 0: self.cell[x][y] = Cell(Type().ground, Type().forest)
                elif pixel[x, y][0] == 50: self.cell[x][y] = Cell(Type().ground, Type().steppe)
                elif pixel[x, y][0] == 100: self.cell[x][y] = Cell(Type().ground, Type().mountain)
                elif pixel[x, y][0] == 255: self.cell[x][y] = Cell(Type().void)
                self.unit[x][y].type = Type().void
                self.building[x][y].type = Type().void
        
        image = Image.new("RGBA", (self.plates_size[0] * self.size[0], self.plates_size[1] * self.size[1]), (255, 255, 255))
        pixel = image.load()

        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                cell_l = self.cell[x][y]
                for _x in range(x * self.plates_size[0], min((x + 1) * self.plates_size[0], image.size[0])):
                    for _y in range(y * self.plates_size[1], min((y + 1) * self.plates_size[1], image.size[1])):
                        if cell_l.type == Type().void: clr = self.imageVoid[0].get_at((_x % self.plates_size[0], _y % self.plates_size[1]))
                        else: clr = self.imageGround[cell_l.subType].get_at((_x % self.plates_size[0], _y % self.plates_size[1]))
                        pixel[_x, _y] = (clr[0], clr[1], clr[2], clr[3])

        image.save("source/pattern/bg.png")
        self.background = pygame.image.load("source/pattern/bg.png")

        self.clearStepBuffer()


    def render(self, screen):

        self.renderInterface(screen)
        self.renderPlace(screen)
        self.renderArea(screen)
        self.renderSelect(screen)
        self.renderMoveRange(screen)
        self.renderAttackRange(screen)
        self.renderBuilding(screen)
        self.renderLevel(screen)
        self.renderUnit(screen)

    def renderInterface(self, screen):
        # группа
        group = pygame.sprite.Group()
        screen.fill((255, 255, 255))
        
        self.renderCellInfo(screen)
        self.renderUnitInfo(screen)
        self.renderBuildingInfo(screen)
        self.renderPlayerInfo(screen)

        # отрисовка
        group.draw(screen)
        
    def renderCellInfo(self, screen):
        # информация о клетке
        AboutCell = pygame.font.Font(None, 25)
        text = list()
        
        text.append("    ___КЛЕТКА___")
        text.append("         Позиция: {} {}".format(self.selectedPos[0], self.selectedPos[1]))
        text.append("         Тип местности: {}".format(self.cell[self.selectedPos[0]][self.selectedPos[1]].decryptionType()))
        text.append("         Принадлежит: {}".format(self.cell[self.selectedPos[0]][self.selectedPos[1]].decryptionTeam()))
        
        for i in range(len(text)):
            
            screen.blit(AboutCell.render(text[i], False, (0, 0, 0)) , (
                0, 
                35 + i * 35
            ))

    def renderUnitInfo(self, screen):
        # информация о ините
        AboutCell = pygame.font.Font(None, 25)
        text = list()
        
        if self.unit[self.selectedPos[0]][self.selectedPos[1]].type != Type().void:
            text.append("    ___ПЕШКА___")
            text.append("         Тип : {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].decryptionType()))
            text.append("         Уровень: {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].decryptionLevel()))
            text.append("         Принадлежит: {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].decryptionTeam()))
            text.append("         Урон: {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].damage()))
            text.append("         Защита: {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].health()))
            text.append("         Радиус атаки: {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].attackRange()))
            text.append("         Радиус перемещения: {}".format(self.unit[self.selectedPos[0]][self.selectedPos[1]].moveRange()))
        
        for i in range(len(text)):
            
            screen.blit(AboutCell.render(text[i], False, (0, 0, 0)) , (
                0, 
                210 + i * 35
            ))

    def renderBuildingInfo(self, screen):
        AboutCell = pygame.font.Font(None, 25)
        text = list()
        
        if self.building[self.selectedPos[0]][self.selectedPos[1]].type != Type().void:
            text.append("    ___ПОСТРОЙКА___")
            text.append("         Тип : {}".format(self.building[self.selectedPos[0]][self.selectedPos[1]].decryptionType()))
            text.append("         Уровень: {}".format(self.building[self.selectedPos[0]][self.selectedPos[1]].decryptionLevel()))
            text.append("         Принадлежит: {}".format(self.building[self.selectedPos[0]][self.selectedPos[1]].decryptionTeam()))
        
        for i in range(len(text)):
            
            screen.blit(AboutCell.render(text[i], False, (0, 0, 0)) , (
                0, 
                210 + i * 35
            ))

    def renderPlayerInfo(self, screen):
        AboutCell = pygame.font.Font(None, 25)
        text = list()
        
        text.append("    ___ИГРОК___")
        text.append("         Тип : {}".format(self.player.decryptionTeam()))
        text.append("         Деньги: {}".format(self.player.money()))
        text.append("         Дерево: {}".format(self.player.resources()[0]))
        text.append("         Камень: {}".format(self.player.resources()[1]))
        text.append("         Провизия: {}".format(self.player.resources()[2]))
        
        for i in range(len(text)):
            
            screen.blit(AboutCell.render(text[i], False, (0, 0, 0)) , (
                0, 
                510 + i * 35
            ))

    def renderPlace(self, screen):
        screen.blit(self.background, (self.sideShift, 0))

    def renderArea(self, screen):
        # области игроков
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.cell[x][y].team != Type().void:
                    rect = (int(x * self.plates_size[0]) + self.sideShift, int(y * self.plates_size[1])) 
                    screen.blit(self.imageArea[0][self.cell[x][y].team - 1], rect)

    def renderSelect(self, screen):
        if self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected == True:
            rect = (int(self.selectedPos[0] * self.plates_size[0]) + self.sideShift, int(self.selectedPos[1] * self.plates_size[1])) 
            screen.blit(self.select, rect)
        
    def renderMoveRange(self, screen):
        # поле перемещения персонажа
        if 0 <= self.selectedPos[0] < self.size[0] and 0 <= self.selectedPos[1] < self.size[1]:
            x0 = self.selectedPos[0]
            y0 = self.selectedPos[1]
            if self.unit[x0][y0].type != Type().void:
                if self.cell[x0][y0].isSelected:
                    # закрашиваем все клетки в "радиусе"
                    for _y in range(y0 - self.unit[x0][y0].moveRange(), y0 + self.unit[x0][y0].moveRange() + 1):
                        for _x in range(x0 - self.unit[x0][y0].moveRange(), x0 + self.unit[x0][y0].moveRange() + 1):
                            try:
                                # если клетка - вода без дороги, то не красим
                                if self.cell[_x][_y].type == Type().void and self.building[_x][_y].type != Type().road: continue 
                                
                                # если на клетке есть юнит или здание то не закрашиваем
                                elif self.unit[_x][_y].type != Type().void or self.building[_x][_y].type != Type().void: continue
                                
                                else:
                                    rect = (_x * self.plates_size[0] + 1 + self.sideShift, _y * self.plates_size[1] + 1)
                                    screen.blit(self.freeCell, rect)
                                    
                            except: pass

    def renderAttackRange(self, screen):
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

                                if self.unit[_x][_y].type != Type().void:
                                    rect = (_x * self.plates_size[0] + 1 + self.sideShift, _y * self.plates_size[1] + 1)
                                    image =  self.occupiedCell[0 if self.unit[_x][_y].team != self.unit[x0][y0].team else 1]
                                    screen.blit(image, rect)
                                    
                                elif self.building[_x][_y].type != Type().void:
                                    rect = (_x * self.plates_size[0] + 1 + self.sideShift, _y * self.plates_size[1] + 1)
                                    image =  self.occupiedCell[0 if self.building[_x][_y].team != self.unit[x0][y0].team else 1]
                                    screen.blit(image, rect)
                                
                            except: pass

    def renderUnit(self, screen):
        # отрисовка окружения поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.unit[x][y].type != Type().void:
                    rect = (int(x * self.plates_size[0]) + self.sideShift, int(y * self.plates_size[1]))
                    image = self.imageUnit[self.unit[x][y].type - 1][self.unit[x][y].team - 1]
                    screen.blit(image, rect)

    def renderBuilding(self, screen):
        # отрисовка окружения поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                # строения
                if self.building[x][y].type != Type().void and self.building[x][y].type != Type().road:
                    image = self.imageBuilding[self.building[x][y].type - 1][self.building[x][y].team - 1]
                    rect = (int(x * self.plates_size[0]) + self.sideShift, int(y * self.plates_size[1]))
                    screen.blit(image, rect)
                # дорога
                elif self.building[x][y].type == Type().road:
                    # матрица с ситуацией на поле 
                    piece = [[False, False, False], [False, True, False], [False, False, False]]
                    try: 
                        if self.building[x][y - 1].type == Type().road: piece[0][1] = True
                    except: pass
                    try: 
                        if self.building[x - 1][y].type == Type().road: piece[1][0] = True
                    except: pass
                    try: 
                        if self.building[x + 1][y].type == Type().road: piece[1][2] = True
                    except: pass
                    try: 
                        if self.building[x][y + 1].type == Type().road: piece[2][1] = True
                    except: pass
                    # принимаем тип дороги
                    rect = (int(x * self.plates_size[0]) + self.sideShift, int(y * self.plates_size[1]))
                    screen.blit(self.imageRoad[Building().indexOfRoadPiece(piece)], rect)

    def renderLevel(self, screen):
        # отрисовка окружения поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):                
                # юниты
                if self.unit[x][y].type != Type().void:
                    rect = (int(x * self.plates_size[0]) + self.sideShift, int(y * self.plates_size[1]))
                    image = self.levelImage[self.unit[x][y].subType]
                    # у юнитов есть тень
                    screen.blit(self.shadowImage, rect)
                    screen.blit(image, rect)
                    
                # здания
                elif self.building[x][y].type != Type().void and self.building[x][y].type != Type().road:
                    rect = (int(x * self.plates_size[0]) + self.sideShift, int(y * self.plates_size[1]))
                    image = self.levelImage[self.building[x][y].subType]
                    screen.blit(image, rect)


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # задаем координаты мышки
            if event.type == pygame.MOUSEMOTION:
                x = (event.pos[0] - self.sideShift) // self.plates_size[0]
                y = (event.pos[1]) // self.plates_size[1]
                self.mousePos = (x, y)

            # задаем селект
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    if 0 <= self.mousePos[0] < self.size[0] and 0 <= self.mousePos[1] < self.size[1]:
                        x = min(self.mousePos[0], self.size[0] - 1)
                        y = min(self.mousePos[1], self.size[1] - 1)
                        self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected = False
                        self.cell[x][y].isSelected = True
                        self.selectedPos = (x, y)

            if event.type == pygame.KEYDOWN:
                
                x = min(self.mousePos[0], self.size[0] - 1)
                y = min(self.mousePos[1], self.size[1] - 1)

                # спавн персонажей (временно)
                if event.key == pygame.K_0: self.spawnUnit(Unit(Type().worker, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_1: self.spawnUnit(Unit(Type().saber, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_2: self.spawnUnit(Unit(Type().assassin, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_3: self.spawnUnit(Unit(Type().berserker, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_4: self.spawnUnit(Unit(Type().archer, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_5: self.spawnUnit(Unit(Type().caster, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_6: self.spawnUnit(Unit(Type().rider, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_7: self.spawnUnit(Unit(Type().lancer, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_8: self.spawnUnit(Unit(Type().tower, 0, self.player.thisPlayer()), (x, y))
                #спавн зданий (временно)
                if event.key == pygame.K_F1: self.spawnBuilding(Building(Type().plate, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_F2: self.spawnBuilding(Building(Type().barracks, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_F3: self.spawnBuilding(Building(Type().farm, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_F4: self.spawnBuilding(Building(Type().quarry, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_F5: self.spawnBuilding(Building(Type().sawmill, 0, self.player.thisPlayer()), (x, y))
                if event.key == pygame.K_F6: self.spawnBuilding(Building(Type().road, 0, self.player.thisPlayer()), (x, y))

                # захватить/покинуть клетку
                if event.key == pygame.K_s: self.cell[x][y].team = self.player.thisPlayer()
                if event.key == pygame.K_d: self.cell[x][y].team = Type().void

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

                # отдать ход следующему игроку
                if event.key == pygame.K_n: 
                    print("next player: {}".format(self.player.nextPlayer()))
                    self.logic()
                    self.clearStepBuffer()
                    self.cell[self.selectedPos[0]][self.selectedPos[1]].isSelected = False
    
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
                    
        self.loadToStepBuffer()
    
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
        
        self.loadToStepBuffer()              

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

        # если ходим в воду, при этом на воде нет дороги
        if self.cell[x][y].type == Type().void and self.building[x][y].type != Type().road: return

        # если место свободно
        if self.unit[x][y].type == Type().void:
            self.unit[x][y] = unit
            # юниты уничтожают здания 
            if self.building[x][y].type != Type().road: self.building[x][y].type = Type().void
            
        self.loadToStepBuffer()

    def spawnBuilding(self, building, To):
        x = To[0]
        y = To[1]

        # если место свободно
        if self.unit[x][y].type == Type().void and self.building[x][y].type == Type().void:
            # если пренадлежит игроку
            if self.cell[x][y].team == self.player.thisPlayer(): self.building[x][y] = building 
            elif self.cell[x][y].type == Type().void and building.type == Type().road: self.building[x][y] = building 
        
        self.loadToStepBuffer()


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
