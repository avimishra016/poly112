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
            self.length = ((x-self.endpoint1[0])**2 +
                        (y-self.endpoint1[1])**2)**0.5
            if self.length < self.maxLen:
                self.endpoint2 = (x,y)
            else:
                yLen = self.endpoint1[1]-y
                xLen = self.endpoint1[0]-x
                theta = math.atan2(yLen, xLen)
                xLen = math.cos(theta)*self.maxLen
                yLen = math.sin(theta)*self.maxLen
                self.endpoint2 = self.endpoint1[0]-xLen, self.endpoint1[1]-yLen

    def getCost(self):
        return self.ppm/50 * self.length

    def placePiece(self):
        self.placed = True
    
    def isPlaced(self):
        return self.placed

#################################################
# Subclasses - Types of pieces 
# Road, Wood, Steel, etc
#################################################
# 1 meter -> 50 pixels
# $200 -> 50 pixels
# $4 -> pixel
class Road(piece):
    def __init__(self, v1):
        super().__init__(100, 'sienna', 200, v1)

class Wood(piece):
    def __init__(self, v1):
        super().__init__(100, 'yellow', 180, v1)

class Steel(piece):
    def __init__(self, v1):
        super().__init__(200, 'grey42', 450, v1)

#################################################
# Vertex Class (Will implement soon)
#################################################
class Vertex:
    def __init__(self, cx, cy, radius = 10):
        self.cx = cx
        self.cy = cy
        self.radius = radius