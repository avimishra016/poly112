from extra import *
from piece import *
################################
# Vehicle class
################################
# A vehicle is a special instance of a vertex as it 
# inherits the same methods for phyics, however it can 
# run on other pieces and has a mass to create force
class Vehicle(Vertex):
    def __init__ (self, x, y, mass = 10, vel = 1):
        super().__init__(x,y, mass, 25)
        self.vel = vel

    def isTouching(self, terrain, roads):
        bottom = self.pos[1]-self.radius
        xLoc = self.pos[0]
        #Touching terrain
        for dirt in terrain:
            top = dirt.getTop()
            if isTangent(top[0], top[1], self.pos, self.radius):
                return dirt
        #Touching Road
        for road in roads:
            if road.getXBounds()[0] < self.pos[0] < road.getXBounds()[1]:
                if isTangent(road.endpoint1.pos, road.endpoint2.pos, self.pos, self.radius):
                    return road
        return None
    
    def moveRight(self):
        self.oldpos = self.pos
        self.pos[0] += self.vel