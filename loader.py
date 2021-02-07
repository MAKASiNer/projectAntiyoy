import pygame


PLATES_SIZE = (33, 33)

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
        # player 1
        [
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl1_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl2_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl3_pl1.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl1_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl2_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl3_pl1.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl1_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl2_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl3_pl1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl4_pl1.png"), PLATES_SIZE)
            ]
        ],
        # player 2
        [
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl1_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl2_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl3_pl2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl1_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl2_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl3_pl2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl1_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl2_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl3_pl2.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl4_pl2.png"), PLATES_SIZE)
            ]
        ],
        # player 3
        [
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl1_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl2_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl3_pl3.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl1_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl2_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl3_pl3.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl1_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl2_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl3_pl3.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl4_pl3.png"), PLATES_SIZE)
            ]
        ],
        # player 4
        [
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl1_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl2_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/worker_lvl3_pl4.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl1_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl2_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/saber_lvl3_pl4.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/assassin2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/berserker2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/archer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/caster2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/rider2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer0.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer1.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/lancer2.png"), PLATES_SIZE)
            ],
            [
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl1_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl2_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl3_pl4.png"), PLATES_SIZE),
                pygame.transform.scale(pygame.image.load("source/texture/unit/tower_lvl4_pl4.png"), PLATES_SIZE)
            ]
        ]
    ],
    # 3
    [
        pygame.transform.scale(pygame.image.load("source/texture/building/plate.png"), PLATES_SIZE),
        pygame.transform.scale(pygame.image.load("source/texture/building/barracks.png"), PLATES_SIZE),
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
    ]
]