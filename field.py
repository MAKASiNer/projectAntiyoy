from PIL import Image, ImageDraw 
from cell import Type, Cell

import math
import random
import pygame
import datetime



class Field:
    def __init__(self, size, playerCount):
        # игра
        self.size = size                        # размеры поля в (КЛЕТКИ по х, КЛЕТКИ по у)
        self.playerCount = playerCount          # количество игроков

        # поле
        self.cell = [[Cell() for _ in range(size[1])] for _ in range(size[0])]
        # размеры
        self.plates_size = (32, 32)       
        # [0] - пустота, [1] - кортеж земель, [2] - кортеж юнитов, [3] - кортеж зданий, [4] - кортеж окружений   
        self.plates_image = [
            [
                pygame.transform.scale(pygame.image.load("source/textures/void.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1))
            ], 
            [
                pygame.transform.scale(pygame.image.load("source/textures/forest.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
                pygame.transform.scale(pygame.image.load("source/textures/mountain.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
                pygame.transform.scale(pygame.image.load("source/textures/steppe.png"), (self.plates_size[0] - 1, self.plates_size[1] - 1)),
            ]
        ]
    
    def generateMap(self, 
        seed=None, 
        peakCount=None, 
        peakRadius=None, 
        peakVerticesRange=None, 
        peakVerticesCount=None,
        holeCount=None, 
        holeRadius=None, 
        holeVerticesRange=None, 
        holeVerticesCount=None
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
        '''

        # сид генерации
        if seed == None: self.seed = datetime.datetime.now().microsecond
        else: self.seed = seed
        random.seed = self.seed

        # количество опорных точек пиков
        if peakCount == None: self.peakCount = random.randint(2, 5)
        else: self.peakCount = peakCount

        # диапазон радиусов опорных точек пиков
        if peakRadius == None: self.peakRadius = (300, 600)
        else: self.peakRadius = peakRadius

        # диапазон колебаний длин направлений пиков
        if peakVerticesRange == None: self.peakVerticesRange = (-300, +400)
        else: self.peakVerticesRange = peakVerticesRange

        # количество направлений пиков
        if peakVerticesCount == None: self.peakVerticesCount = random.randint(3, 12)
        else: self.peakVerticesCount = random.randint(peakVerticesCount[0], peakVerticesCount[1])

        # количество опорных точек дырок
        if holeCount == None: self.holeCount = random.randint(0, 15)
        else: self.holeCount = holeCount

        # диапазон радиусов опорных точек дырок
        if holeRadius == None: self.holeRadius = (50, 200)
        else: self.holeRadius = holeRadius

        # диапазон колебаний длин направлений дырок
        if holeVerticesRange == None: self.holeVerticesRange = (-300, +400)
        else: self.holeVerticesRange = holeVerticesRange

        # количество направлений дырок
        if holeVerticesCount == None: self.holeVerticesCount = random.randint(3, 12)
        else: self.holeVerticesCount = random.randint(holeVerticesCount[0], holeVerticesCount[1])

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
            pattern.polygon(coord, fill=(255, 255, 255))

        image.save("source/pattern/pattern_step_1.png")
        # делим изображение сеткой, и закрашиваем в черный
        for x in range(0, image.size[0], int(image.size[0] / self.size[0])):
            for y in range(0, image.size[1], int(image.size[1] / self.size[1])):
                clr = 0
                for _x in range(x, min(x + int(image.size[0] / self.size[0]), image.size[0])):
                    for _y in range(y, min(y + int(image.size[1] / self.size[1]), image.size[1])):
                        clr += (pixel[_x, _y])[0]
                clr = int(clr / (int(image.size[0] / self.size[0]) * int(image.size[1] / self.size[1])))
                clr = (0, 0, 0) if clr < 255 / 2 else (255, 255, 255)
                for _x in range(x, min(x + int(image.size[0] / self.size[0]), image.size[0])):
                    for _y in range(y, min(y + int(image.size[1] / self.size[1]), image.size[0])):
                        pixel[_x, _y] = clr
                
                if clr == (0, 0, 0):
                    self.cell[int(x * self.size[0] / 2000)][int(y * self.size[1] / 2000)] = Cell(Type().ground)
                elif clr == (255, 255, 255):
                    self.cell[int(x * self.size[0] / 2000)][int(y * self.size[1] / 2000)] = Cell(Type().void, clr)

        image.save("source/pattern/pattern_step_2.png")

    def render(self, screen):
        group = pygame.sprite.Group()

        # отрисовка клеток поля
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                sprite = pygame.sprite.Sprite()
                sprite.rect = (int(x * self.plates_size[0]), int(y * self.plates_size[1]))

                # пустые клетки
                if self.cell[x][y].type == Type().void:
                    sprite.image = self.plates_image[0][0]
                    group.add(sprite)
                
                # земля
                if self.cell[x][y].type == Type().ground:
                    sprite.image = self.plates_image[1][self.cell[x][y].subType]
                    group.add(sprite)
        
        group.draw(screen)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    x = event.pos[0] // self.plates_size[0]
                    y = event.pos[1] // self.plates_size[1]
                    self.cell[x][y].subType = (self.cell[x][y].subType + 1) % 3
                    print(x, y)