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
    
    def moveRight(self):
        self.oldpos = self.pos
        self.pos[0] += self.vel
    def update(self, collidingPiece):
        super().update(collidingPiece)
        self.velocity[1]*=1.01