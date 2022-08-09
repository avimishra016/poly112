#################################################
# pieces.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from cmu_112_graphics import *
from extra import *
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

    def setEndpoint2(self, x, y, vertices, joints):
        if not self.placed:
            self.length = ((x-self.endpoint1.pos[0])**2 +
                        (y-self.endpoint1.pos[1])**2)**0.5
            if self.length < self.maxLen:
                self.endpoint2 = checkVertexExists(vertices,joints,Vertex(x,y))
            else:
                yLen = self.endpoint1.pos[1]-y
                xLen = self.endpoint1.pos[0]-x
                theta = math.atan2(yLen, xLen)
                xLen = math.cos(theta)*self.maxLen
                yLen = math.sin(theta)*self.maxLen
                newVertex = Vertex(self.endpoint1.pos[0]-xLen, self.endpoint1.pos[1]-yLen)
                self.endpoint2 = checkVertexExists(vertices, joints, newVertex)

    def getCost(self):
        return self.ppm/50 * self.length

    def placePiece(self):
        self.placed = True
        return self.endpoint2
    
    def isPlaced(self):
        return self.placed

    def update(self):
        '''
        dx = self.endpoint2.pos[0]-self.endpoint1.pos[0]
        dy = self.endpoint2.pos[1]-self.endpoint1.pos[1]
        distance = (dx**2 + dy**2)**0.5
        difference = (self.length - distance) / distance
        offsetX = dx * difference/2
        offsetY = dy * difference/2
        if not isinstance(self.endpoint1, StaticJoint):
            self.endpoint1.pos[0] += offsetX
            self.endpoint1.pos[1] += offsetY
        if not isinstance(self.endpoint2, StaticJoint):
            self.endpoint2.pos[0] += offsetX
            self.endpoint2.pos[1] += offsetY
        '''
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
# Vertex Class 
#################################################
class Vertex:
    def __init__(self, cx, cy, radius = 10):
        self.originalPos = [cx,cy]
        self.pos = [cx, cy]
        self.oldpos = [cx, cy]
        self.gravity = [0,4]
        self.radius = radius

    def resetPos(self):
        self.pos[0] = self.originalPos[0]
        self.pos[1] = self.originalPos[1]

    def update(self):
        vel = (self.oldpos[0]-self.pos[0], self.oldpos[1]-self.pos[1])
        self.oldpos = self.pos
        self.pos[0] += vel[0] + self.gravity[0]
        self.pos[1] += vel[1] + self.gravity[1]
#################################################
# Static Joint Class (Will implement soon)
#################################################

class StaticJoint:
    def __init__(self, cx, cy, radius = 10):
        self.pos = (cx, cy)
        self.radius = radius