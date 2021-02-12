import pygame



class Button:
    def __init__(self, rect, key=None):
        self.key = key
        self.rect = rect

        self.pos0 = None
        self.pos1 = None
        
        self.imageHold = pygame.transform.scale(pygame.image.load("source/interface/TestButtonHold.png"), self.rect[1])
        self.ImagePress = pygame.transform.scale(pygame.image.load("source/interface/TestButtonPress.png"), self.rect[1])
        self.imageSelect = pygame.transform.scale(pygame.image.load("source/interface/TestButtonSelect.png"), self.rect[1])

    def draw(self, screen):
        group = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.rect = self.rect

        if 0 <= pygame.mouse.get_pos()[0] - self.rect[0][0] < self.rect[1][0] and\
            0 <= pygame.mouse.get_pos()[1] - self.rect[0][1] < self.rect[1][1]:
            if self.pos1 != None: 
                if 0 <= self.pos1[0] - self.rect[0][0] < self.rect[1][0] and\
                    0 <= self.pos1[1] - self.rect[0][1] < self.rect[1][1]: sprite.image = self.ImagePress
                else: sprite.image = self.imageSelect
            else: sprite.image = self.imageSelect
        else: sprite.image = self.imageHold

        group.add(sprite)
        group.draw(screen)

    def pushUp(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pos0 == None:
                self.pos0 = pygame.mouse.get_pos()
        else:
            if 0 <= pygame.mouse.get_pos()[0] - self.rect[0][0] < self.rect[1][0] and\
                0 <= pygame.mouse.get_pos()[1] - self.rect[0][1] < self.rect[1][1]:        
                if self.pos0 != None:
                    if 0 <= self.pos0[0] - self.rect[0][0] < self.rect[1][0] and\
                        0 <= self.pos0[1] - self.rect[0][1] < self.rect[1][1]:
                        self.pos0 = None
                        return True             
            else: self.pos0 = None
        return False
    
    def pushDown(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pos1 == None:
                self.pos1 = pygame.mouse.get_pos()
                if 0 <= pygame.mouse.get_pos()[0] - self.rect[0][0] < self.rect[1][0] and\
                    0 <= pygame.mouse.get_pos()[1] - self.rect[0][1] < self.rect[1][1]:
                    return True

        else: self.pos1 = None
        return False