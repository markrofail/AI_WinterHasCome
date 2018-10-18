from enum import IntFlag


class Cell(IntFlag):
    EMPTY = 0
    OBSTACLE = 1
    DRAGON_STONE = 2
    WHITE_WALKER = 3
    JON = 4
