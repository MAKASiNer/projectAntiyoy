import pygame


PLATES_SIZE = (40, 40)

IMAGE = [
    # 0
    [
        pygame.transform.scale(pygame.image.load("source/texture/void.png"), PLATES_SIZE)
    ], 
    # 1
    [
        pygame.transform.scale(pygame.image.load("source/texture/ground/steppe.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/ground/forest.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/ground/mountain.png"), PLATES_SIZE),
    ],
    # 2
    [
        pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl1_pl1.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/saber.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/assassin.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/berserker.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/archer.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/caster.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/rider.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/lancer.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/unit/tower.png"), PLATES_SIZE)
    ],
    # 3
    [
        pygame.transform.scale(pygame.image.load("source/texture/building/plate_pl1.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/barracks_lvl1_pl1.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/farm.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/quarry.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/sawmill_lvl1_pl1.png"), PLATES_SIZE)
    ],
    # 4
    [
        pygame.transform.scale(pygame.image.load("source/texture/building/road0.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road1.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road2.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road3.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road4.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road5.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road6.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road7.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road8.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road9.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road10.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road11.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road12.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road13.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road14.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/road15.png"), PLATES_SIZE)
    ],
    # 5
    [
        pygame.transform.scale(pygame.image.load("source/interface/area.png"), PLATES_SIZE)
    ]
]