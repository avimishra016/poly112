#################################################
# vehicle.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from extra import *
from piece import *
################################
# Vehicle class
################################
# A vehicle is a special instance of a vertex as it 
# inherits the same methods for phyics, however it can 
# run on other pieces and has a mass to create force
class Vehicle(Vertex):
    def __init__ (self, x, y, mass = 10, vel = 1.425):
        super().__init__(x,y, mass, 25)
        self.vel = vel

    #checks if the vehicle is touching terrain or a road
    def isTouching(self, terrain, roads):
        bottom = self.pos[1]-self.radius
        xLoc = self.pos[0]
        #Touching terrain
        for dirt in terrain:
            top = dirt.getTop()
            if (isTangent(top[0], top[1], self.pos, self.radius) 
                and top[0][1] > self.pos[1]):
                self.velocity[1] = self.originalVelocity[1]
                return dirt
        #Touching Road
        for road in roads:
            if road.getXBounds()[0] < self.pos[0] < road.getXBounds()[1]:
                v1 = road.endpoint1.pos
                v2 = road.endpoint2.pos
                if isTangent(v1, v2, self.pos, self.radius):
                    self.velocity[1] = self.originalVelocity[1]
                    return road
        return None

    #moves the vehicle
    def update(self, collidingPiece):
        if collidingPiece == None:
            super().update()
        else: 
            self.velocity[0] = self.vel
            self.oldpos = self.pos
            self.pos[0] += self.vel
            v1, v2 = 0, 0
            if isinstance(collidingPiece, Terrain):
                v1, v2 = collidingPiece.getTop()
                self.pos[1] += getSlope(v1, v2) / self.vel -1
            else:
                v1 = collidingPiece.endpoint1.pos
                v2 = collidingPiece.endpoint2.pos
                slope = getSlope(v1,v2)
                self.pos[1] += getSlope(v1, v2) / self.vel - 3
        self.velocity[1]*=1.01