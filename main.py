from field import Field

import pygame



if __name__ == '__main__':
    field = Field((25, 25), 1)
    field.generateMap()

    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    while True:
        field.event()
        field.render(screen)
        pygame.display.flip()
    pygame.quit()