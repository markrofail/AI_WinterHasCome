import numpy as np

from src.models.cell import Cell
from src.models.jon import Jon


class Components:
    white_walkers = None
    obstacles = None
    dragon_stone = None

    def __init__(self, white_walkers=[], obstacles=[], dragon_stone=[]):
        self.white_walkers = white_walkers
        self.obstacles = obstacles
        self.dragon_stone = dragon_stone


class Grid:
    cells = None
    jon = None

    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.cells = np.full(shape=(self.m, self.n), fill_value=Cell.EMPTY)
        self.components = Components()

    # ######################################################
    # Generation Methods
    # ######################################################

    def update(self):
        """recreates grid"""
        # clear grid
        self.cells = np.full(shape=(self.m, self.n), fill_value=Cell.EMPTY)

        # fill with respective cell types
        if self.components.white_walkers:
            for location in self.components.white_walkers:
                self.cells[location] = Cell.WHITE_WALKER

        if self.components.obstacles:
            for location in self.components.obstacles:
                self.cells[location] = Cell.OBSTACLE

        if self.components.dragon_stone:
            self.cells[self.components.dragon_stone] = Cell.DRAGON_STONE

        if self.jon.location:
            self.cells[self.jon.location] = Cell.JON

    def init_jon(self, location, capacity, dragon_glass=0):
        self.jon = Jon(
            location=location,
            capacity=capacity,
            dragon_glass=dragon_glass
        )
        self.update()

    def fill_with(self, fill_type, count=None):
        """fills grid with count items of fill_type"""
        if count is None:
            count = np.random.randint(1, 10)

        locations = list()

        while count > 0:
            x = np.random.randint(0, self.m)
            y = np.random.randint(0, self.n)
            if self.cells[x, y] == Cell.EMPTY:
                locations.append((x, y))
                count -= 1

        if fill_type == Cell.WHITE_WALKER:
            self.components.white_walkers = locations
        if fill_type == Cell.OBSTACLE:
            self.components.obstacles = locations
        if fill_type == Cell.DRAGON_STONE:
            self.components.dragon_stone = locations[0]
        self.update()

    # ######################################################
    # Query Methods
    # ######################################################

    def cell_type_at(self, location):
        if self.is_in_bounds(location):
            return self.cells[location]

    def is_dragon_glass(self, location):
        return self.cell_type_at(location) == Cell.DRAGON_STONE

    def is_obstacle(self, location):
        return self.cell_type_at(location) == Cell.OBSTACLE

    def is_white_walker(self, location):
        return self.cell_type_at(location) == Cell.WHITE_WALKER

    def is_safe_location(self, location):
        target_cell_type = self.cell_type_at(location)
        unsafe_cell_types = [Cell.WHITE_WALKER, Cell.OBSTACLE, None]

        safe_cell = target_cell_type not in unsafe_cell_types
        within_bounds = self.is_in_bounds(location)

        return safe_cell and within_bounds

    def is_in_bounds(self, location):
        x, y = location
        valid_x = (0 <= x < self.m)
        valid_y = (0 <= y < self.n)
        return valid_x and valid_y

    def nearby_white_walkers(self, location):
        x, y = location
        test_locations = [
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1)
        ]
        return [x for x in test_locations if x in self.components.white_walkers]

    def remove_white_walkers(self, location):
        ww_locations = self.nearby_white_walkers(location)
        self.components.white_walkers = [x for x in self.components.white_walkers if x not in ww_locations]
        self.update()

    # ######################################################
    # Interface Methods
    # ######################################################

    def move_jon(self, location):
        self.jon.move(location)

        if self.is_dragon_glass(location):
            self.jon.replenish()
        self.update()

    def kill_white_walkers(self):
        self.remove_white_walkers(self.jon.location)
        self.jon.use_dragon_glass()

    # ######################################################
    # Class Methods
    # ######################################################

    def __str__(self):
        self.update()

        cell_str = dict([
            (Cell.EMPTY, ' '),
            (Cell.WHITE_WALKER, 'W'),
            (Cell.OBSTACLE, 'X'),
            (Cell.DRAGON_STONE, 'D'),
            (Cell.JON, 'J')
        ])

        res = 'm→\nn↓'

        for i in range(self.n):
            res += ' {} '.format(str(chr(i + ord('A'))))
        res += '\n'

        count = 0
        for row in self.cells:
            res += '{} '.format(count)
            for cell in row:
                res += '[{}]'.format(cell_str[cell])
            res += '\n'
            count += 1
        return res

    def __hash__(self):
        return hash(self.cells)

    def __eq__(self, other):
        return np.array_equal(self.cells, other.cells)

    def __lt__(self, other):
        return self.cells < other.cells
