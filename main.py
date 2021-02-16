from game import Game


import os
import pygame
import datetime



if __name__ == '__main__':
    game = Game((20, 20), 4, (1800, 800))
    game.generateMap()
    
    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    while True:
        time1 = datetime.datetime.now()
        
        game.render(screen)
        game.event()
        pygame.display.flip()
        
        time2 = datetime.datetime.now()
        print("\033[H\033[J")
        print(1000000 / (time2.microsecond - time1.microsecond))  
        
        
    pygame.quit()