import numpy as np

from src.models.cell import Cell
from src.models.grid import Grid


def gen_grid():
    # initialize an empty grid
    m, n = np.random.randint(4, 10, size=(2,))
    grid = Grid(m, n)

    # place Jon at m, n
    grid.init_jon(
        location=(m - 1, n - 1),
        capacity=np.random.randint(1, 10),
    )

    # fill with white walkers and obstacles
    grid.fill_with(Cell.WHITE_WALKER)
    grid.fill_with(Cell.OBSTACLE)

    # place one dragon stone randomly
    grid.fill_with(Cell.DRAGON_STONE, count=1)

    return grid


if __name__ == '__main__':
    gen_grid()
