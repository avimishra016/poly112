#################################################
# extra.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
import math
#checks the distance between two points
def distance(x1, y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

#checks if two circles are intersecting
def circlesIntersect(dist, r):
    return dist <= 2*r

#gets the distance between two vertices
def distanceBetVertices(v1, v2):
    return distance(v1.pos[0], v1.pos[1],
                    v2.pos[0], v2.pos[1])

#gets whether two vertices intersect or not
def verticesIntersect(v1, v2):
    d = distanceBetVertices(v1, v2)
    return circlesIntersect(d, v1.radius)

#checks if a vertex exists in a list
def checkVertexExists(vertices, joints, v):
    for vertex in vertices:
        if (verticesIntersect(vertex, v)):
            return vertex
    for joint in joints:
        if (verticesIntersect(joint, v)):
            return joint
    return v

#resets the position of all the vertices
def resetVertices(vertices):
    for vertex in vertices:
        vertex.resetPos()

#checks if a point is on a line segment
def pointOnLine(v1, v2, point):
    lengthLine = distance(v1[0], v1[1], v2[0], v2[1])
    d1 = distance(point[0], point[1], v1[0], v1[1])
    d2 = distance(point[0], point[1], v2[0], v2[1])
    return abs(lengthLine-(d1+d2)) < 0.01

#inspiration: http://www.jeffreythompson.org/collision-detection/line-circle.php
#check if a line between two points is tangent to a circle
def isTangent(v1, v2, circle, radius):
    lengthLine = distance(v1[0], v1[1], v2[0], v2[1])
    dotProd = ( ( (circle[0]-v1[0]) * (v2[0]-v1[0]) ) + 
                ( (circle[1]-v1[1]) * (v2[1]-v1[1]) ) ) / (lengthLine**2)
    closestX = v1[0] + (dotProd * (v2[0]-v1[0]))
    closestY = v1[1] + (dotProd * (v2[1]-v1[1]))
    dist = distance(closestX, closestY, circle[0], circle[1])
    return dist <= radius + 2 and pointOnLine(v1, v2, (closestX, closestY))

#get the slope between two vertices
def getSlope(v1, v2):
    return (v2[1]-v1[1]) / (v2[0]-v1[0])