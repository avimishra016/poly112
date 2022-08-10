#################################################
# app.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from cmu_112_graphics import *
from pieces import *
from extra import *

#################################################
# Model
#################################################

def appStarted(app):
    app.budget = 30000
    app.phase = 'build'
    app.timerDelay = 10
    app.staticJoints = {StaticJoint(115, app.height*2/3), 
                        StaticJoint(app.width-115, app.height*2/3)}
    reset(app)

def reset(app):
    app.price = 0
    app.pieces = {'Road': set(), 'Wood': set(), 'Steel': set()}
    app.currPieceType = 'Road'
    app.currPiece = None    
    app.inPreview = False
    app.vertices = set()
    app.currVertex = None
##################################################
# Controller
#################################################
def timerFired(app):
    if app.phase == 'run':
        for vertex in app.vertices:
            vertex.update()
        for value in app.pieces.values():
            for piece in value:
                piece.update()
# Change Pieces
def keyPressed(app, event):
    if app.phase == 'build':
        if event.key == '1':
            app.currPieceType = 'Road'
        if event.key == '2':
            app.currPieceType = 'Wood'
        if event.key == '3':
            app.currPieceType = 'Steel'

# Create a starting point for the piece
# When clicked a second time place the piece on the screen
def mousePressed(app, event):
    if (event.x >= app.width-90 and event.x <= app.width-30 and
        event.y <= 90 and event.y >= 30):
        if app.phase != 'run':
            app.phase = 'run'
        else:
            app.phase = 'build'
            resetVertices(app.vertices)
    
    if app.phase == 'build':
        if (event.x >= 30 and event.x<= 90 and
            event.y >=30 and event.y <= 90):
            reset(app)

        if event.y > app.height/36 + 100:
            app.inPreview = not app.inPreview
            if app.inPreview:
                app.currVertex = checkVertexExists(app.vertices, app.staticJoints, 
                                                    Vertex(event.x,event.y))
                if not isinstance(app.currVertex, StaticJoint):
                    app.vertices.add(app.currVertex)
                if app.currPieceType == 'Road':
                    app.currPiece = Road(app.currVertex)
                elif app.currPieceType == 'Wood':
                    app.currPiece = Wood(app.currVertex)
                elif app.currPieceType == 'Steel':
                    app.currPiece = Steel(app.currVertex)
            else:
                app.currVertex = checkVertexExists(app.vertices, app.staticJoints, 
                                                    app.currPiece.placePiece())
                if not isinstance(app.currVertex, StaticJoint):
                    app.vertices.add(app.currVertex)
                app.price += app.currPiece.getCost()
                app.pieces[app.currPieceType].add(app.currPiece)
                app.currPiece = None

# display preview for placing
def mouseMoved(app, event):
    if app.phase == 'build':
        if app.inPreview:
            app.currPiece.setEndpoint2(event.x, event.y, app.vertices, app.staticJoints)

#################################################
# View
#################################################

# Draws Blue Background
def drawBackgroud(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'lightskyblue3')
    canvas.create_rectangle(0 , 0, app.width, app.height/36 + 100, 
                            fill = 'black')

# Draws budget in red if over budget
# Draws budget in green if under budget
def drawBudget(app, canvas):
    color = 'red'
    if app.price < app.budget:
        color = 'forestgreen'
    canvas.create_text(app.width/2, app.height/40, 
                        text = f'${"{:.2f}".format(app.price)}', font = 'Shruti 34 bold',
                        anchor = 'n', fill = color)
    canvas.create_text(app.width/2, app.height/36 + 50,
                        text = f'Budget: ${app.budget}', font = 'Shruti 21',
                        anchor = 'n', fill = 'yellow')

# Draws all the placed pieces                   
def drawPieces(app, canvas):
    for type in app.pieces:
        for piece in app.pieces[type]:
            x1 = piece.endpoint1.pos[0]
            y1 = piece.endpoint1.pos[1]
            x2 = piece.endpoint2.pos[0]
            y2 = piece.endpoint2.pos[1]
            canvas.create_line(x1,y1,x2,y2, fill = piece.color, width = 5)

# Draws the preview for the current piece
def drawPreview(app, canvas):
    if app.inPreview and app.currPiece.endpoint2 != None:
        x1 = app.currPiece.endpoint1.pos[0]
        y1 = app.currPiece.endpoint1.pos[1]
        x2 = app.currPiece.endpoint2.pos[0]
        y2 = app.currPiece.endpoint2.pos[1]
        canvas.create_line(x1,y1,x2,y2,fill = 'navajowhite', width = 5)

# draw button to delete all pieces
def drawDeleteAllPieces(app, canvas):
    canvas.create_line(30,30, 90, 90, fill = 'red', width = 10)
    canvas.create_line(90,30, 30, 90, fill = 'red', width = 10)

# draws button to pause and play
def drawPausePlay(app, canvas):
    if app.phase == 'build':
        canvas.create_polygon(app.width-90, 30,
                            app.width-90, 90,
                            app.width-30, 60,
                            fill = 'green3')
    if app.phase == 'run':
        canvas.create_line(app.width-80, 30,
                           app.width-80, 90,
                           width = 10, fill = 'plum3')
        canvas.create_line(app.width-40, 30,
                           app.width-40, 90,
                           width = 10, fill = 'plum3')
def drawLevel(app, canvas):
    canvas.create_rectangle(0, app.height*2/3, 
                            115, app.height, 
                            fill = 'lightsalmon4', outline = 'lightsalmon4')
    canvas.create_rectangle(app.width, app.height, 
                            app.width-115, app.height*2/3, 
                            fill = 'lightsalmon4', outline = 'lightsalmon4')

def drawVertices(app, canvas):
    for vertex in app.vertices:
        canvas.create_oval(vertex.pos[0]-vertex.radius, vertex.pos[1]-vertex.radius,
                           vertex.pos[0]+vertex.radius, vertex.pos[1]+vertex.radius,
                           fill = 'yellow', outline = 'black')
def drawStaticJoints(app, canvas):
    for joint in app.staticJoints:
        canvas.create_oval(joint.pos[0]-joint.radius, joint.pos[1]-joint.radius,
                           joint.pos[0]+joint.radius, joint.pos[1]+joint.radius,
                           fill = 'red', outline = 'black')
def redrawAll(app, canvas):
    drawBackgroud(app,canvas)
    drawBudget(app,canvas)
    drawDeleteAllPieces(app,canvas)
    drawPausePlay(app,canvas)
    drawLevel(app, canvas)
    drawPreview(app,canvas)
    drawPieces(app,canvas)
    drawVertices(app,canvas)
    drawStaticJoints(app, canvas)

runApp(width = 700, height = 700)