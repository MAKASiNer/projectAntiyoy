from game import Game
from menue import Menue, Button

import pygame



def mainMenue(game, screen):
    
    mMenue = Menue(((0, 0), game.winSize))
    mMenue.addButton(Button(((700, 150), (200, 200))))
    mMenue.addButton(Button(((700, 300), (200, 200))))
    mMenue.addButton(Button(((700, 450), (200, 200))))
    
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
    mMenue.addButton(Button(((700 + 200, 500), (200, 200))))
    mMenue.addButton(Button(((700, 500), (200, 200))))
    mMenue.addButton(Button(((700 - 200, 500), (200, 200))))
    
    # миниатюра
    image = pygame.transform.scale(pygame.image.load("source/pattern/bg.png"), (300, 300))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # принять
        if mMenue.buttonList[0].check()[1]: break
        # сгенерировать из сохранений
        if mMenue.buttonList[1].check()[1]: 
            game.createBg()
        # генерация нового мира
        if mMenue.buttonList[2].check()[1]: 
            game.generateMap()
            game.createBg()
            image = pygame.transform.scale(pygame.image.load("source/pattern/bg.png"), (300, 300))
        
        mMenue.render(screen)
        screen.blit(image, (650, 100))
        pygame.display.flip()



if __name__ == '__main__':
    game = Game((20, 20), 4, (1800, 800))
    
    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    mainMenue(game, screen)

    while True:       
        game.render(screen)
        game.event()
        pygame.display.flip() 
                   
    pygame.quit()