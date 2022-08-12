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
    drawBackground(app, canvas, False)
    canvas.create_text(app.width/2, app.height/3, text='Welcome to Poly112', 
                       font = font, fill = 'yellow')
    canvas.create_text(app.width/2 ,app.height/3 + 100,
                        fill = 'White', text='(Click anywhere on the screen to play)', 
                        font = 'arial 26')
    drawLevel(app,canvas)
    drawStaticJoints(app,canvas)

def splashScreenMode_mousePressed(app, event):
    app.mode = 'gameMode'
##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    font = 'Rupee 36 bold'
    text = 'so be sure to make ur build less expensive Have fun Playing Poly112!'
    drawBackground(app, canvas, False)
    canvas.create_text(20, 20, text='Welcome to Poly112', 
                       font = font, fill = 'yellow', anchor = 'nw')
    canvas.create_text(20, 90, text = 'In this game (Poly112) you will be designing your own bridge!',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 120, text = 'To win the game you must design your bridge in such a way that',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 150, text = 'the ball goes across the bridge without falling.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 180, text = 'Explore your options!', font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 210, text = 'Use different support pieces, try making jumps, anything that',
                       font = 'arial 17', anchor = 'nw') 
    canvas.create_text(20, 240, text = 'you believe would make a cool looking bridge.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 270, text = 'After you have passed making one bridge, terrain at new heights',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 300, text = 'will be made and you can make another bridge.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 330, text = 'If you fall off the bridge at any point, you would have to redo',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 360, text = 'the level and not get new terrain.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 390, text = 'Be warned, if you go overbudget you will have to redo the level as',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 420, text = 'well, so be sure to make ur build less expensive.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 450, text = 'Have fun playing Poly112!!!',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 490, text = 'You can switch your piece by using the keys 123 or by',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 520, text = 'clicking on the pieces in the bottom left.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 550, text = 'Clicking on the red X will clear all your pieces.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 580, text = 'However, clicking on the yellow x will clear all pieces',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 610, text = 'connected to the selected vertex.',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(20, 640, text = 'Test your bridge with the green play button. Have Fun!',
                       font = 'arial 17', anchor = 'nw')
    canvas.create_text(app.width/2 ,app.height,
                        fill = 'White', text='(Click anywhere on the screen to resume)', 
                        font = 'arial 20', anchor = 's')

def helpMode_mousePressed(app, event):
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
    #Updates terrain Variables
    resetTerrain(app)
    #updates teh bridge variables
    resetBridge(app)
    #resets basic game variables
    reset(app)

def resetTerrain(app):
    # Creates and stores the Terrain for the Level
    if app.mode == 'splashScreenMode':
        height1 = 467
        height2 = 467
    # Generates random heights and assigns it to the terrain
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
    #0, app.height-100, 250, app.height
    app.previewPieces = (Road(Vertex(20, app.height-70), Vertex(70, app.height-20)),
                         Wood(Vertex(90, app.height-70), Vertex(140, app.height-20)),
                         Steel(Vertex(160, app.height-70), Vertex(210, app.height-20))
                        )
# Model Veriables that Need to be reset whenever you clear the screen
def reset(app):
    # Makes the current piece a road
    app.currPieceType = 'Road'
    #No current piece has been created
    app.currPiece = None    
    #Variable that tracks if you need to draw a preview or not
    app.inPreview = False
    # Stores the current vertex to be drawn
    app.currVertex = None
    #Manages which phase of the game you are in
    app.phase = 'build'
    # Creates a vehicle for the game
    app.vehicle = Vehicle(50, 200)
    app.gameOver = False
    app.gameOverCondition = ''
def resetBridge(app):
    #How much money you have used so far
    app.price = 0
    #Stores the pieces
    app.pieces = {'Road': set(), 'Wood': set(), 'Steel': set()}
    #Stores all the vertices
    app.vertices = set()
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
        #Check for win conditions
        if app.vehicle.pos[1] > app.height:
            app.gameOver = True
            app.gameOverCondition = 'Vehicle fell out of map'
        if (app.vehicle.pos[0] + app.vehicle.radius >= app.width
            and app.vehicle.pos[1] < app.terrain[1].topLeft[1]):
            app.gameOver = True
            app.vehicle.velocity = [0,0]
            #Check if user has crossed the bridge without going overbudget
            if app.price <= app.budget:
                app.gameOverCondition = 'You have crossed the bridge!!!'
            else:
                app.gameOverCondition = 'Overbudget'

# Change Pieces and reset
def gameMode_keyPressed(app, event):
    if app.phase == 'build' and not app.gameOver:
        #Allows user to change pieces with numbers
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
        #resets the game depending on the win condition
        if event.key == 'r':
            app.gameOver = False
            if app.gameOverCondition == 'You have crossed the bridge!!!':
                resetTerrain(app)
                resetBridge(app)
            app.gameOverCondition = ''
            resetVertices(app.vertices)
            reset(app)

#Gets you the current piece in preview
def getCurrPiece(app):
    if not isinstance(app.currVertex, StaticJoint):
        app.vertices.add(app.currVertex)
    if app.currPieceType == 'Road':
        app.currPiece = Road(app.currVertex)
    elif app.currPieceType == 'Wood':
        app.currPiece = Wood(app.currVertex)
    elif app.currPieceType == 'Steel':
        app.currPiece = Steel(app.currVertex)

# Create a starting point for the piece
# When clicked a second time place the piece on the screen
def gameMode_mousePressed(app, event):
    #Check if game is over
    if app.gameOver: return
    #check if user clicked on question mark, if so go to help mode
    if app.width-189 <= event.x <= app.width-126 and 22 <= event.y <= 103:
        app.mode = 'helpMode'
    #check if user clicked on the pause play button
    if (event.x >= app.width-90 and event.x <= app.width-30 and
        event.y <= 90 and event.y >= 30):
        #if they clicked play, change the game phase and reset certain variables
        if app.phase != 'run':
            app.phase = 'run'
            app.currVertex = None
            if app.inPreview:
                app.inPreview = False
        #if they clicked pause, reset the variables
        else:
            app.phase = 'build'
            resetVertices(app.vertices)
            app.vehicle.resetPos()
    if app.phase == 'build':
        #check if the user is using the buttons in the bottom left to change pieces
        if event.x >= 0 and event.x <= 230 and event.y >= app.height-100:
            app.inPreview = False
            app.currVertex = None
            if 20 <= event.x <= 70:
                app.currPieceType = 'Road'
            if 90 <= event.x <= 140:
                app.currPieceType = 'Wood'
            if 160 <= event.x <= 210:
                app.currPieceType = 'Steel'
        # Check if user clicked the red x, if so delete all pieces
        elif (event.x >= 30 and event.x<= 90 and
            event.y >=30 and event.y <= 90):
            reset(app)
            resetBridge(app)
        # check if user clicked the yellow x,
        # if so delete all pieces connected to the current vertex
        elif (event.x >= 120 and event.x<= 180 and
            event.y >=30 and event.y <= 90) and app.currVertex!=None:
            for mat, pieces in app.pieces.items():
                copyPieces = pieces.copy()
                for piece in copyPieces:
                    if piece.endpoint1 == app.currVertex:
                        app.pieces[mat].remove(piece)
                        app.price -= piece.getCost()
                    if piece.endpoint2 == app.currVertex:
                        app.pieces[mat].remove(piece)
                        app.price -= piece.getCost()
            if not isinstance(app.currVertex, StaticJoint):
                app.vertices.remove(app.currVertex)
            app.currVertex = None
            app.inPreview = False
        # get the new vertex if clicked on screen
        elif event.y > app.height/36 + 100:
            app.inPreview = not app.inPreview
            if app.inPreview:
                app.currVertex = checkVertexExists(app.vertices, app.staticJoints, 
                                                    Vertex(event.x,event.y))
                getCurrPiece(app)
            else:
                app.currVertex = checkVertexExists(app.vertices, app.staticJoints, 
                                                    app.currPiece.placePiece())
                if not isinstance(app.currVertex, StaticJoint):
                    app.vertices.add(app.currVertex)
                app.price += app.currPiece.getCost()
                app.pieces[app.currPieceType].add(app.currPiece)
                getCurrPiece(app)
                #app.currPiece = None
                app.inPreview = True

# changes the preview depending on the mouse location
def gameMode_mouseMoved(app, event):
    if app.phase == 'build' and not app.gameOver:
        if app.inPreview:
            app.currPiece.setEndpoint2(event.x, event.y, app.vertices, app.staticJoints)



#################################################
# View
#################################################

# Draws Blue Background and black box
def drawBackground(app, canvas, blackBox = True):
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

# Draws all the placed pieces on the board                 
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
    if app.inPreview and app.currPiece != None and app.currPiece.endpoint2 != None:
        x1 = app.currPiece.endpoint1.pos[0]
        y1 = app.currPiece.endpoint1.pos[1]
        x2 = app.currPiece.endpoint2.pos[0]
        y2 = app.currPiece.endpoint2.pos[1]
        canvas.create_line(x1,y1,x2,y2,fill = 'navajowhite', width = 5)

# draw button to delete all pieces
def drawDeleteAllPieces(app, canvas):
    canvas.create_line(30,30, 90, 90, fill = 'red', width = 10)
    canvas.create_line(90,30, 30, 90, fill = 'red', width = 10)

# draws the button to delet all pieces connected to the current vertex
def drawDeleteConnected(app, canvas):
    canvas.create_line(120,30, 180, 90, fill = 'yellow', width = 10)
    canvas.create_line(180,30, 120, 90, fill = 'yellow', width = 10)

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

#draws the terrain for the level
def drawLevel(app, canvas):
    for terrain in app.terrain:
        x1, y1 = terrain.topLeft 
        x2, y2 = terrain.bottomRight
        canvas.create_rectangle(x1, y1, x2, y2,
                                fill = 'lightsalmon4', outline = 'lightsalmon4')
#draws the vehicle or ball
def drawVehicle(app, canvas):
    cx, cy = app.vehicle.pos
    r = app.vehicle.radius
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = 'seagreen1')
#draws all the vertices
def drawVertices(app, canvas):
    for vertex in app.vertices:
        canvas.create_oval(vertex.pos[0]-vertex.radius, vertex.pos[1]-vertex.radius,
                           vertex.pos[0]+vertex.radius, vertex.pos[1]+vertex.radius,
                           fill = 'yellow', outline = 'black')
# draws the current vertex selected
def drawCurrVertex(app, canvas):
    if app.currVertex != None:
        x1 = app.currVertex.pos[0]-app.currVertex.radius-5
        y1 = app.currVertex.pos[1]-app.currVertex.radius-5
        x2 = app.currVertex.pos[0]+app.currVertex.radius+5
        y2 = app.currVertex.pos[1]+app.currVertex.radius+5
        canvas.create_oval(x1, y1, x2, y2,
                           fill = 'gold1', outline = 'gold1')
#draws the static joints
def drawStaticJoints(app, canvas):
    for joint in app.staticJoints:
        canvas.create_oval(joint.pos[0]-joint.radius, joint.pos[1]-joint.radius,
                           joint.pos[0]+joint.radius, joint.pos[1]+joint.radius,
                           fill = 'red', outline = 'black')
#draws the game over screen
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

#draws the piece select menu in the bottom left
def drawPieceSelectPreview(app, canvas):
    if app.phase == 'build':
        canvas.create_rectangle(0, app.height-100, 230, app.height, fill = 'beige', outline = 'beige')
        if app.currPieceType == 'Road':
            x1 = app.previewPieces[0].endpoint1.pos[0]
            y1 = app.previewPieces[0].endpoint1.pos[1]
            x2 = app.previewPieces[0].endpoint2.pos[0]
            y2 = app.previewPieces[0].endpoint2.pos[1]
            canvas.create_oval(x1,y1,x2,y2, fill = 'grey79', outline = 'grey79')
        elif app.currPieceType == 'Wood':
            x1 = app.previewPieces[1].endpoint1.pos[0]
            y1 = app.previewPieces[1].endpoint1.pos[1]
            x2 = app.previewPieces[1].endpoint2.pos[0]
            y2 = app.previewPieces[1].endpoint2.pos[1]
            canvas.create_oval(x1,y1,x2,y2, fill = 'grey79', outline = 'grey79')
        elif app.currPieceType == 'Steel':
            x1 = app.previewPieces[2].endpoint1.pos[0]
            y1 = app.previewPieces[2].endpoint1.pos[1]
            x2 = app.previewPieces[2].endpoint2.pos[0]
            y2 = app.previewPieces[2].endpoint2.pos[1]
            canvas.create_oval(x1,y1,x2,y2, fill = 'grey79', outline = 'grey79')
        for piece in app.previewPieces:
            x1 = piece.endpoint1.pos[0]
            y1 = piece.endpoint1.pos[1]
            x2 = piece.endpoint2.pos[0]
            y2 = piece.endpoint2.pos[1]
            canvas.create_line(x1,y1,x2,y2, fill = piece.color, width = 5)

# draws the button to go to the help menu
def drawHelpMenu(app, canvas):
    canvas.create_text(app.width-160, 60, text = '?', 
                       font = 'Shruti 62 bold', fill = 'yellow')

def gameMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawHelpMenu(app, canvas)
    drawBudget(app, canvas)
    drawDeleteAllPieces(app, canvas)
    drawDeleteConnected(app, canvas)
    drawPausePlay(app, canvas)
    drawLevel(app, canvas)
    drawPreview(app, canvas)
    drawVehicle(app, canvas)
    drawPieces(app, canvas)
    drawCurrVertex(app,canvas)
    drawVertices(app, canvas)
    drawStaticJoints(app, canvas)
    drawPieceSelectPreview(app, canvas)
    if app.gameOver:
        drawGameOver(app, canvas)
runApp(width = 700, height = 700)