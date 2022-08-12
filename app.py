#################################################
# app.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from cmu_112_graphics import *
from piece import *
from extra import *
from joints import *
from vehicle import *
from terrain import *
import random

##########################################
# Splash Screen Mode
##########################################
def splashScreenMode_redrawAll(app, canvas):
    font = 'Rupee 36 bold'
    drawBackgroud(app, canvas, False)
    canvas.create_text(app.width/2, app.height/3, text='Welcome to Poly112', 
                       font = font, fill = 'yellow')
    canvas.create_text(app.width/2 ,app.height/3 + 100,
                        fill = 'White', text='(Click anywhere on the screen to play)', 
                        font = 'arial 26')
    drawLevel(app,canvas)
    drawStaticJoints(app,canvas)

def splashScreenMode_mousePressed(app, event):
    app.mode = 'gameMode'
#################################################
# Model
#################################################

def appStarted(app):
    # How much you can spend on the bridge
    app.mode = 'splashScreenMode'
    app.budget = 30000
    #Manages which phase of the game you are in
    #How often timerFired runs
    app.timerDelay = 1
    resetTerrain(app)
    reset(app)

def resetTerrain(app):
    # Creates and stores the Terrain for the Level
    if app.mode == 'splashScreenMode':
        height1 = 467
        height2 = 467
    else:
        height1 = random.randint(230,550)
        height2 = random.randint(230,550)
    app.terrain = ( Terrain(0, height1, 115, app.height), 
                    Terrain(app.width-115, height2, app.width, app.height)
                  )
    # Creates and stores the Static Joints for the Level
    app.staticJoints = ( StaticJoint(115, height1), 
                         StaticJoint(app.width-115, height2)
                        )

# Model Veriables that Need to be reset whenever you clear the screen
def reset(app):
    #How much money you have used so far
    app.price = 0
    #Stores the pieces
    app.pieces = {'Road': set(), 'Wood': set(), 'Steel': set()}
    # Makes the current piece a road
    app.currPieceType = 'Road'
    #No current piece has been created
    app.currPiece = None    
    #Variable that tracks if you need to draw a preview or not
    app.inPreview = False
    #Stores all the vertices
    app.vertices = set()
    # Stores the current vertex to be drawn
    app.currVertex = None
    #Manages which phase of the game you are in
    app.phase = 'build'
    # Creates a vehicle for the game
    app.vehicle = Vehicle(50, 200)
    app.gameOver = False
    app.gameOverCondition = ''


##################################################
# Controller / Game Mode
#################################################
def gameMode_timerFired(app):
    #onl execute when in run phase
    if app.phase == 'run' and not app.gameOver:
        #update the position of the vertices
        for vertex in app.vertices:
            vertex.update()
        #update the pieces
        for value in app.pieces.values():
            for piece in value:
                 piece.update()
        #update the vehicles position
        seg = app.vehicle.isTouching(app.terrain, app.pieces['Road'])
        app.vehicle.update(seg)
        if app.vehicle.pos[1] > app.height:
            app.gameOver = True
            app.gameOverCondition = 'Vehicle fell out of map'
        if (app.vehicle.pos[0] + app.vehicle.radius >= app.width
            and app.vehicle.pos[1] < app.terrain[1].topLeft[1]):
            app.gameOver = True
            app.vehicle.velocity = [0,0]
            if app.price <= app.budget:
                app.gameOverCondition = 'You have crossed the bridge!!!'
            else:
                app.gameOverCondition = 'Overbudget'

# Change Pieces
def gameMode_keyPressed(app, event):
    if app.phase == 'build' and not app.gameOver:
        if event.key in '123':
            app.inPreview = False
            app.currVertex = None
            if event.key == '1':
                app.currPieceType = 'Road'
            if event.key == '2':
                app.currPieceType = 'Wood'
            if event.key == '3':
                app.currPieceType = 'Steel'
    if app.gameOver:
        if event.key == 'r':
            app.gameOver = False
            if app.gameOverCondition == 'You have crossed the bridge!!!':
                resetTerrain(app)
            app.gameOverCondition = ''
            reset(app)

# Create a starting point for the piece
# When clicked a second time place the piece on the screen
def gameMode_mousePressed(app, event):
    if app.gameOver: return
    if (event.x >= app.width-90 and event.x <= app.width-30 and
        event.y <= 90 and event.y >= 30):
        if app.phase != 'run':
            app.phase = 'run'
            if app.inPreview:
                app.inPreview = False
                #app.vertices.remove(app.currVertex)
        else:
            app.phase = 'build'
            resetVertices(app.vertices)
            app.vehicle.resetPos()
    
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
def gameMode_mouseMoved(app, event):
    if app.phase == 'build' and not app.gameOver:
        if app.inPreview:
            app.currPiece.setEndpoint2(event.x, event.y, app.vertices, app.staticJoints)



#################################################
# View
#################################################

# Draws Blue Background
def drawBackgroud(app, canvas, blackBox = True):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'lightskyblue3')
    if blackBox:
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
    for terrain in app.terrain:
        x1, y1 = terrain.topLeft 
        x2, y2 = terrain.bottomRight
        canvas.create_rectangle(x1, y1, x2, y2,
                                fill = 'lightsalmon4', outline = 'lightsalmon4')
def drawVehicle(app, canvas):
    cx, cy = app.vehicle.pos
    r = app.vehicle.radius
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'seagreen1')

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

def drawGameOver(app, canvas):
        newText = 'press r to try again'
        if app.gameOverCondition == 'You have crossed the bridge!!!':
            newText = 'press r to make a new bridge'
            color = 'forestgreen'
        else:
            color = 'red'
        canvas.create_text(app.width/2, app.height/2, 
                           text = app.gameOverCondition, fill = color,
                           font = 'Shruti 36 bold')
        canvas.create_text(app.width/2, app.height/2 + 50, text = newText,
                            fill = color, font = 'Arial 22')
def gameMode_redrawAll(app, canvas):
    drawBackgroud(app, canvas)
    drawBudget(app, canvas)
    drawDeleteAllPieces(app, canvas)
    drawPausePlay(app, canvas)
    drawLevel(app, canvas)
    drawPreview(app, canvas)
    drawVehicle(app, canvas)
    drawPieces(app, canvas)
    drawVertices(app, canvas)
    drawStaticJoints(app, canvas)
    if app.gameOver:
        drawGameOver(app, canvas)
runApp(width = 700, height = 700)