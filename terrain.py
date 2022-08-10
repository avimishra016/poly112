class Terrain:
    def __init__(self, x1, y1, x2, y2):
        self.topLeft = (x1, y1)
        self.bottomRight = (x2, y2)

    def getTop(self):
        return self.topLeft, (self.bottomRight[0], self.topLeft[1])