from game import Game
from menue import Menue, Button

import pygame



def mainMenue(game, screen):
    
    mMenue = Menue(((0, 0), game.winSize))
    mMenue.addButton(Button(((700, 150), (400, 200)), "ИГРАТЬ"))
    mMenue.addButton(Button(((700, 300), (400, 200)), "СОЗДАТЬ МИР"))
    mMenue.addButton(Button(((700, 450), (400, 200)), "ВЫХОД"))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # кнопка старта
        if mMenue.buttonList[0].check()[1]: break
        # открыть генератор мира
        if mMenue.buttonList[1].check()[1]: settingMap(game, screen)
        # кнопка выхода
        if mMenue.buttonList[2].check()[1]: pygame.quit()
        
        mMenue.render(screen)
        pygame.display.flip() 

def settingMap(game, screen):
    
    mMenue = Menue(((0, 0), game.winSize))
    mMenue.addButton(Button(((700, 150), (400, 200)), "СГЕНЕРИРОВАТЬ"))
    mMenue.addButton(Button(((700, 300), (400, 200)), "ПРИНЯТЬ"))
    mMenue.addButton(Button(((700, 450), (400, 200)), "НАЗАД"))
    
    # миниатюра
    image = pygame.transform.scale(pygame.image.load("source/pattern/bg.png"), (400, 400))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # генерация нового мира
        if mMenue.buttonList[0].check()[1]: 
            game.generateMap()
            game.createBg()
            image = pygame.transform.scale(pygame.image.load("source/pattern/bg.png"), (400, 400))
        # сгенерировать из сохранений
        if mMenue.buttonList[1].check()[1]: 
            game.createBg()
        # принять
        if mMenue.buttonList[2].check()[1]: break 
            
        
        mMenue.render(screen)
        screen.blit(image, (150, 150))
        pygame.display.flip()

def stopMenue(game, screen):
    mMenue = Menue(((0, 0), game.winSize))
    mMenue.addButton(Button(((700, 150), (400, 200)), "ПРОДОЛЖИТЬ"))
    mMenue.addButton(Button(((700, 300), (400, 200)), "..."))
    mMenue.addButton(Button(((700, 450), (400, 200)), "ВЫХОД"))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # продолжить
        if mMenue.buttonList[0].check()[1]: return
        # ...
        if mMenue.buttonList[1].check()[1]: pass
        # выход
        if mMenue.buttonList[2].check()[1]: return 1
            
        
        mMenue.render(screen)
        pygame.display.flip()



if __name__ == '__main__':
    game = Game((6, 6), 4, (1800, 800))
    
    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    mainMenue(game, screen)

    while True:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]: 
            if stopMenue(game, screen) == 1: mainMenue(game, screen)
        
        game.render(screen)
        game.event()
        pygame.display.flip() 
                   
    pygame.quit()