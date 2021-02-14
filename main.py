from game import Game

import pygame



if __name__ == '__main__':
    game = Game((20, 20), 4, (1800, 800))
    game.generateMapV2()
    
    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    while True:
        game.render(screen)
        game.event()
        pygame.display.flip()
    pygame.quit()