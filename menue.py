from button import Button

import pygame



class Menue:
    def __init__(self, rect=None):
        if rect == None: self.rect = ((0, 0), (0, 0))
        else: self.rect = rect
        
        self.image = pygame.transform.scale(pygame.image.load("source/interface/background.png"), self.rect[1])
        self.buttonList = list()
                
    def addButton(self, button):
        self.buttonList.append(button)
        
    def render(self, screen):
        screen.blit(self.image, self.rect[0])
        for btn in self.buttonList: btn.draw(screen)