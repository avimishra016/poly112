#################################################
# joints.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from turtle import pos
from piece import *
from extra import *
from terrain import *
#################################################
# Vertex Class 
#################################################
class Vertex:
    def __init__(self, cx, cy, mass = 1, radius = 10, vel = 0, gravity = 0.5):
        # Store original position for later reset
        self.originalPos = [cx,cy]

        #Store position and old position (Physics implementation)
        self.pos = [cx, cy]
        self.oldpos = [cx, cy]

        self.vel = vel

        #Store the velocity (how many pixels the object moves)
        self.originalVelocity = [0,gravity]
        self.velocity = [0, gravity]

        #Store the radius of the vertex (For user interaction)
        self.radius = radius

        #Create mass
        self.mass = mass

    def resetPos(self):
        self.pos = self.originalPos.copy()
        self.oldpos = self.originalPos.copy()
        self.velocity = self.originalVelocity.copy()

    def update(self, collidingSegment):
        self.oldpos = self.pos
        if collidingSegment == None:
            vel = (self.pos[0]-self.oldpos[0], self.pos[1]-self.oldpos[1])
            self.oldpos = self.pos
            self.pos[0] += vel[0] + self.velocity[0]
            self.pos[1] += vel[1] + self.velocity[1]
        else:
            self.velocity[0] = self.vel
            self.oldpos = self.pos
            self.pos[0] += self.vel
            v1, v2 = 0, 0
            if isinstance(collidingSegment, Terrain):
                v1, v2 = collidingSegment.getTop()
                self.pos[1] += getSlope(v1, v2) / self.vel -1
            else:
                v1 = collidingSegment.endpoint1.pos
                v2 = collidingSegment.endpoint2.pos
                self.pos[1] += getSlope(v1, v2) / self.vel - 3

#################################################
# Static Joints
#################################################

class StaticJoint:
    def __init__(self, cx, cy, radius = 10):
        self.pos = (cx, cy)
        self.radius = radius