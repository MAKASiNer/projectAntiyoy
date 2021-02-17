from game import Game
from menue import Menue, Button

import pygame



if __name__ == '__main__':
    game = Game((20, 20), 4, (1800, 800))
    game.generateMap()
    
    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)
    
    mainMenue = Menue(((0, 0), game.winSize))
    mainMenue.addButton(Button(((700, 300), (200, 200))))

    while True:
        
        game.render(screen)
        game.event()
        
        a = mainMenue.buttonList[0].check()
        if a[0] or a[1]: print(a)
        
        mainMenue.render(screen)
        pygame.display.flip() 
       
               
    pygame.quit()