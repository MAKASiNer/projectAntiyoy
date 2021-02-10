from game import Game

import pygame



if __name__ == '__main__':
    game = Game((30, 30), 4, (1600, 990))
    #game.generateMapV1()
    game.generateMapV2()
    
    pygame.init()
    pygame.display.set_caption('ⒹⓊⓇⓀⒶ')
    screen = pygame.display.set_mode(game.winSize)

    while True:
        game.render(screen)
        game.event()
        pygame.display.flip()
    pygame.quit()