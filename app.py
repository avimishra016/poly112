#################################################
# app.py
#
# Your name: Avi Mishra
# Your andrew id: avim
#################################################
from cmu_112_graphics import *
from pieces import *

#################################################
# Model
#################################################

def appStarted(app):
    app.budget = 30000
    app.pieces = {'Road': set(), 'Wood': set(), 'Steel': set()}
    app.currPieceType = 'Road'
    app.currPiece = None
    app.inPreview = False

##################################################
# Controller
#################################################

# Change Pieces
def keyPressed(app, event):
    if event.key == '1':
        app.currPieceType = 'Road'
    if event.key == '2':
        app.currPieceType = 'Wood'
    if event.key == '3':
        app.currPieceType = 'Steel'

# Create a starting point for the piece
# When clicked a second time place the piece on the screen
def mousePressed(app, event):
    app.inPreview = not app.inPreview
    if app.inPreview:
        if app.currPieceType == 'Road':
            app.currPiece = Road((event.x,event.y))
        elif app.currPieceType == 'Wood':
            app.currPiece = Wood((event.x,event.y))
        elif app.currPieceType == 'Steel':
            app.currPiece = Steel((event.x,event.y))
    else:
        app.currPiece.placePiece()
        app.budget -= app.currPiece.getCost()
        app.pieces[app.currPieceType].add(app.currPiece)
        app.currPiece = None

# display preview for placing
def mouseMoved(app, event):
    if app.inPreview:
        app.currPiece.setEndpoint2(event.x, event.y)

#################################################
# View
#################################################

# Draws Blue Background
def drawBackgroud(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'lightskyblue3')

# Draws budget in red if over budget
# Draws budget in green if under budget
def drawBudget(app, canvas):
    color = 'red'
    if app.budget > 0:
        color = 'forestgreen'
    canvas.create_text(app.width/2, app.height/36, 
                        text = f'Budget: ${"{:.2f}".format(app.budget)}', font = 'Shruti 34 bold',
                        anchor = 'n', fill = color)

# Draws all the placed pieces                   
def drawPieces(app, canvas):
    for type in app.pieces:
        for piece in app.pieces[type]:
            x1, y1 = piece.endpoint1
            x2, y2 = piece.endpoint2
            canvas.create_line(x1,y1,x2,y2, fill = piece.color, width = 5)

# Draws the preview for the current piece
def drawPreview(app, canvas):
    if app.inPreview and app.currPiece.endpoint2 != None:
        x1, y1 = app.currPiece.endpoint1
        x2, y2 = app.currPiece.endpoint2
        canvas.create_line(x1,y1,x2,y2,fill = 'orange', width = 5)

def redrawAll(app, canvas):
    drawBackgroud(app,canvas)
    drawBudget(app,canvas)
    drawPreview(app,canvas)
    drawPieces(app,canvas)

runApp(width = 700, height = 700)