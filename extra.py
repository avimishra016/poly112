def distance(x1, y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def circlesIntersect(dist, r):
    return dist <= 2*r

def distanceBetVertices(v1, v2):
    return distance(v1.pos[0], v1.pos[1],
                    v2.pos[0], v2.pos[1])

def verticesIntersect(v1, v2):
    d = distanceBetVertices(v1, v2)
    return circlesIntersect(d, v1.radius)

def checkVertexExists(vertices, joints, v):
    for vertex in vertices:
        if (verticesIntersect(vertex, v)):
            return vertex
    for joint in joints:
        if (verticesIntersect(joint, v)):
            return joint
    return v

def resetVertices(vertices):
    for vertex in vertices:
        vertex.resetPos()