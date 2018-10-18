class Jon:
    def __init__(self, location, capacity, dragon_glass=0):
        self.location = location
        self.capacity = capacity
        self.dragon_glass = dragon_glass

    def move(self, location):
        self.location = location

    def use_dragon_glass(self):
        self.dragon_glass -= 1

    def replenish(self):
        self.dragon_glass = self.capacity

    def __copy__(self):
        return Jon(
            location=self.location,
            capacity=self.capacity,
            dragon_glass=self.dragon_glass
        )
