#################################################
# pieces.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from cmu_112_graphics import *
import math

#################################################
# Piece SuperClass
#################################################
class piece:
    def __init__(self, maxLen, color, ppm, v1):
        self.length = 0
        self.maxLen = maxLen
        self.color = color
        self.ppm = ppm
        self.endpoint1 = v1
        self.endpoint2 = v1
        self.placed = False

    def setEndpoint2(self, x, y):
        if not self.placed:
            self.length = ((x-self.endpoint1.pos[0])**2 +
                        (y-self.endpoint1.pos[1])**2)**0.5
            if self.length < self.maxLen:
                self.endpoint2 = Vertex(x,y)
            else:
                yLen = self.endpoint1.pos[1]-y
                xLen = self.endpoint1.pos[0]-x
                theta = math.atan2(yLen, xLen)
                xLen = math.cos(theta)*self.maxLen
                yLen = math.sin(theta)*self.maxLen
                self.endpoint2 = Vertex(self.endpoint1.pos[0]-xLen, self.endpoint1.pos[1]-yLen)

    def getCost(self):
        return self.ppm/50 * self.length

    def placePiece(self):
        self.placed = True
        return self.endpoint2
    
    def isPlaced(self):
        return self.placed

    def update(self):
        pass
#################################################
# Subclasses - Types of pieces 
# Road, Wood, Steel, etc
#################################################
# 1 meter -> 50 pixels
# $200 -> 50 pixels
# $4 -> pixel
class Road(piece):
    def __init__(self, v1):
        super().__init__(100, 'brown4', 200, v1)

class Wood(piece):
    def __init__(self, v1):
        super().__init__(100, 'goldenrod2', 180, v1)

class Steel(piece):
    def __init__(self, v1):
        super().__init__(200, 'grey42', 450, v1)

#################################################
# Vertex Class (Will implement soon)
#################################################
class Vertex:
    def __init__(self, cx, cy, radius = 10):
        self.pos = (cx, cy)
        self.oldpos = (cx, cy)
        self.gravity = (0,1)
        self.radius = radius
    
    def update(self):
        vel = (self.oldpos[0]-self.pos[0], self.oldpos[1]-self.pos[1])
        self.oldpos = self.pos
        self.pos[0] += vel[0] + self.gravity[0]
        self.pos[1] += vel[1] + self.gravity[1]

