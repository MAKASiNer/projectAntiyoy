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
        pygame.transform.scale(pygame.image.load("source/texture/building/sawmill.png"), PLATES_SIZE)
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



''' расход за ход, найм 1/2/3... лвл '''
UNITEXPENSES = [
    # void lvl  0/0/0 , per step
    [0, 0, 0, 0],
    # worker lvl 1/2/3 , per step
    [2, 3, 3, 3],
    # saber lvl 1/2/3 , per step
    [2, 5, 6, 7],
    # assasin lvl 1/2/3 , per step
    [3, 6, 7, 8],
    # berserker lvl 1/2/3 , per step
    [3, 6, 7, 3],
    # archer lvl 1/2/3 , per step
    [4, 7, 6, 3],
    # caster lvl 1/2/3 , per step
    [4, 9, 10, 3],
    # rider lvl 1/2/3 , per step
    [4, 7, 8, 3],
    # lanser lvl 1/2/3 , per step
    [4, 7, 7, 3],
    # tower lvl 1/2/3/4 , per step
    [12, 15, 17, 24, 31]
]



''' добыча за ход на своей/не своей территории, постройка 1/2/3 лвл '''
BUILDINGEXPENSE = [
    [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0, 0],
    [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0, 0],
    [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0, 0],
    #farm
    [[[6, 7, 9], [3, 4, 5], [0, 0, 0]], 10, 20, 30],
    # quarry
    [[[0, 0, 0], [0, 0, 0], [10, 15, 20]], 40, 70, 100],
    # sawmill 
    [[[2, 3, 5], [5, 6, 8], [1, 1, 2]], 20, 40, 60],
    # road
    [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 5]
]