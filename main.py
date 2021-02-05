from game import Game
from player import Player

import pygame



if __name__ == '__main__':
    game = Game((30, 30), 1, (1300, 1000))
    game.generateMapV2()
    #game.generateMap()
    

    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    while True:
        game.render(screen)
        game.event() 
        pygame.display.flip()
    pygame.quit()