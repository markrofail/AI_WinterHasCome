from copy import deepcopy


class State:
    pass


class SwState(State):

    def __init__(self, grid, dragon_glass=None, white_walkers=None, location=None):
        self.grid = deepcopy(grid)
        self.grid.components = deepcopy(grid.components)

        if location:
            self.grid.move_jon(location)

        if white_walkers:
            self.grid.kill_white_walkers()

        if dragon_glass:
            self.grid.jon_dragon_glass = dragon_glass

    def white_walkers(self):
        return len(self.grid.components.white_walkers)

    def dragon_glass(self):
        return self.grid.jon.dragon_glass

    def location(self):
        return self.grid.jon.location

    def __repr__(self):
        return str(self.grid)

    def __lt__(self, other):
        return self.grid < other.grid

    def __hash__(self):
        return hash((self.location(), self.white_walkers(), self.dragon_glass()))

    def __eq__(self, other):
        return isinstance(other, SwState) \
               and self.location() == other.location() \
               and self.white_walkers() == other.white_walkers() \
               and self.dragon_glass() == other.dragon_glass()
