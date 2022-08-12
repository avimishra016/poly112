#################################################
# piece.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from cmu_112_graphics import *
from extra import *
from joints import *
import math

#################################################
# Piece SuperClass
#################################################
class piece:
    def __init__(self, maxLen, color, ppm, stiffness, v1, v2 = None):
        self.length = 0
        self.maxLen = maxLen
        self.color = color
        self.ppm = ppm
        self.endpoint1 = v1
        self.endpoint2 = v1
        if v2 != None:
            self.endpoint2 = v2
        self.placed = False
        self.stiffness = stiffness

    #sets the second endpoint for preview
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

    #gets the cost of the piece
    def getCost(self):
        return self.ppm/50 * self.length

    #places the piece and updates variables
    def placePiece(self):
        self.placed = True
        self.length = distanceBetVertices(self.endpoint1, self.endpoint2)
        temp = self.endpoint2
        if self.endpoint2.pos[0] < self.endpoint1.pos[0]:
            self.endpoint2 = self.endpoint1
            self.endpoint1 = temp
        return temp
    
    #checks if a piece has been placed
    def isPlaced(self):
        return self.placed

    #gets the x bounds of a piece
    def getXBounds(self):
        return self.endpoint1.pos[0], self.endpoint2.pos[0]

    #updates the piece, so that it falls from gravity
    #doesn't update the vertex position
    def update(self):
        # Inspiration for how the physics work and how it is implemented: 
        # https://gamedevelopment.tutsplus.com/tutorials/simulate-tearable-cloth-and-ragdolls-with-simple-verlet-integration--gamedev-519
        distX = self.endpoint1.pos[0] - self.endpoint2.pos[0]
        distY = self.endpoint1.pos[1] - self.endpoint2.pos[1]
        dist = math.sqrt(distX**2 + distY**2)
        diff = 0
        p1 = 0.5 * self.stiffness
        p2 = self.stiffness - p1
        if dist != 0:
            diff = (self.length - dist) / dist
        if not isinstance(self.endpoint1, StaticJoint):
            self.endpoint1.pos[0] += distX * p1 * diff
            self.endpoint1.pos[1] += distY * p1 * diff
        if not isinstance(self.endpoint2, StaticJoint):
            self.endpoint2.pos[0] -= distX * p2 * diff
            self.endpoint2.pos[1] -= distY * p2 * diff


#################################################
# Subclasses - Types of pieces 
# Road, Wood, Steel, etc
#################################################
# 1 meter -> 50 pixels
# $200 -> 50 pixels
# $4 -> pixel
class Road(piece):
    def __init__(self, v1, v2 = None):
        super().__init__(100, 'brown4', 200, 1, v1, v2)

class Wood(piece):
    def __init__(self, v1, v2 = None):
        super().__init__(100, 'goldenrod2', 180, 1.5, v1, v2)

class Steel(piece):
    def __init__(self, v1, v2 = None):
        super().__init__(200, 'grey42', 450, 2, v1, v2)