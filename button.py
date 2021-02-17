import pygame



class Button:
    def __init__(self, rect, key=None):
        self.key = key
        self.rect = rect

        self.pos0 = None
        self.pos1 = None
        
        self.imageHold = pygame.transform.scale(pygame.image.load("source/interface/TestButtonHold.png"), self.rect[1])
        self.imagePress = pygame.transform.scale(pygame.image.load("source/interface/TestButtonPress.png"), self.rect[1])
        self.imageSelect = pygame.transform.scale(pygame.image.load("source/interface/TestButtonSelect.png"), self.rect[1])

    def draw(self, screen):
        image = self.imageHold

        if 0 <= pygame.mouse.get_pos()[0] - self.rect[0][0] < self.rect[1][0] and\
            0 <= pygame.mouse.get_pos()[1] - self.rect[0][1] < self.rect[1][1]:
            if self.pos1 != None: 
                if 0 <= self.pos1[0] - self.rect[0][0] < self.rect[1][0] and\
                    0 <= self.pos1[1] - self.rect[0][1] < self.rect[1][1]: image = self.imagePress
                else: image = self.imageSelect
            else: image = self.imageSelect
        else: image = self.imageHold

        screen.blit(image, self.rect)

    ''' возвращает ивент о отпуске после нажатия '''
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
                    else:
                        self.pos0 = None
                        return False
            else: self.pos0 = None
        return False
    
    ''' возвращает ивент о нажатие '''
    def pushDown(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pos1 == None:
                self.pos1 = pygame.mouse.get_pos()
                if 0 <= pygame.mouse.get_pos()[0] - self.rect[0][0] < self.rect[1][0] and\
                    0 <= pygame.mouse.get_pos()[1] - self.rect[0][1] < self.rect[1][1]:
                    return True

        else: self.pos1 = None
        return False
    
    ''' возвращает [ивент о нажатие, ивент о отпуске после нажатия] '''
    def check(self):
        return [self.pushDown(), self.pushUp()]