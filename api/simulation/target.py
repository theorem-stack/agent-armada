class Target:
    def __init__(self, id, position, radius):
        self.id = id # int
        self.position = position # np.array([x, y], dtype=float)
        self.radius = radius # int