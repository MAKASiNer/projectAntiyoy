from game import Game
from player import Player

import pygame



if __name__ == '__main__':
    game = Game((10, 10), 1, (1300, 1000))
    game.generateMap()

    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    while True:
        game.render(screen)
        game.event() 
        pygame.display.flip()
    pygame.quit()