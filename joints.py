from piece import *
from extra import *

#################################################
# Vertex Class 
#################################################
class Vertex:
    def __init__(self, cx, cy, mass = 1, radius = 10, gravity = 0.5):
        # Store original position for later reset
        self.originalPos = [cx,cy]

        #Store position and old position (Physics implementation)
        self.pos = [cx, cy]
        self.oldpos = [cx, cy]

        #Store the velocity (how many pixels the object moves)
        self.velocity = [0, gravity]

        #Store the radius of the vertex (For user interaction)
        self.radius = radius

        #Create mass
        self.mass = mass

    def resetPos(self):
        self.pos = self.originalPos.copy()
        self.oldpos = self.originalPos.copy()

    def update(self):
        vel = (self.pos[0]-self.oldpos[0], self.pos[1]-self.oldpos[1])
        self.oldpos = self.pos
        self.pos[0] += vel[0] + self.velocity[0]
        self.pos[1] += vel[1] + self.velocity[1]

#################################################
# Static Joints
#################################################

class StaticJoint:
    def __init__(self, cx, cy, radius = 10):
        self.pos = (cx, cy)
        self.radius = radius