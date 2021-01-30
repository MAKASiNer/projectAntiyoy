from field import Field

import pygame



if __name__ == '__main__':
    field = Field((30, 30), 1, (1300, 1000))
    field.generateMap()

    pygame.init()
    screen = pygame.display.set_mode(field.winSize)

    while True:
        field.event()
        field.render(screen)
        pygame.display.flip()
    pygame.quit()