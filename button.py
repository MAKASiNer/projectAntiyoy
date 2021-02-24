import pygame



class Button:
    def __init__(self, rect, text, key=None):
        self.key = key
        self.rect = rect

        self.pos0 = None
        self.pos1 = None
        
        self.imageHold = pygame.transform.scale(pygame.image.load("source/interface/TestButtonHold.png"), self.rect[1])
        self.imagePress = pygame.transform.scale(pygame.image.load("source/interface/TestButtonPress.png"), self.rect[1])
        self.imageSelect = pygame.transform.scale(pygame.image.load("source/interface/TestButtonSelect.png"), self.rect[1])
        
        self.text = pygame.font.Font(None, 30).render(text, False, (0, 0, 0))
        self.textShift = (self.rect[1][0] / 4, self.rect[1][1] / 2)

    ''' проверяет коллизию кнопки '''
    def collide(self, pos):
        inRect = bool(0 <= pos[0] - self.rect[0][0] < self.rect[1][0] and 0 <= pos[1] - self.rect[0][1] < self.rect[1][1])
        if inRect: return bool(self.imageHold.get_at([pos[0] - self.rect[0][0], pos[1] - self.rect[0][1]])[3] != 0)
        return False

    ''' отрисовывает кнопку '''
    def draw(self, screen):
        image = self.imageHold

        if self.collide(pygame.mouse.get_pos()):
            if self.pos1 != None: 
                if self.collide(self.pos1): image = self.imagePress
                else: image = self.imageSelect
            else: image = self.imageSelect
        else: image = self.imageHold

        screen.blit(image, self.rect)
        screen.blit(self.text, 
                    (self.rect[0][0] + self.textShift[0], 
                     self.rect[0][1] + self.textShift[1]))

    ''' возвращает ивент о отпуске после нажатия '''
    def pushUp(self):
        if pygame.mouse.get_pressed()[0]:
            if self.pos0 == None:
                self.pos0 = pygame.mouse.get_pos()
        else:
            if self.collide(pygame.mouse.get_pos()):
                if self.pos0 != None:
                    if self.collide(self.pos0):
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
                if self.collide(self.pos1): return True
        else: self.pos1 = None
        return False
    
    ''' возвращает [ивент о нажатие, ивент о отпуске после нажатия] '''
    def check(self):
        return [self.pushDown(), self.pushUp()]