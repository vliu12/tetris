from cmu_graphics import *
import random


def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 80
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = 1
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    app.pieceTopRow = 0
    app.nextPieceIndex = 0
    loadNextPiece(app)
    pieceWidth = len(app.piece[0])
    boardWidth = app.cols
    app.pieceLeftCol = (boardWidth - pieceWidth)//2
    app.pieceColor = app.tetrisPieceColors[app.nextPieceIndex]
    app.paused = False
    app.stepsPerSecond = 1 #start mega slow like actual tetris
    app.counter = 0
    app.score = 0
    app.lines = 0
    app.level = 1
    app.gameOver = False
    app.infoScreen = False


def redrawAll(app):
    
    if app.gameOver:
        drawLabel("Game Over", 200, 200, size=40, fill='red', bold=True)
        drawLabel("Press any key to try again!", 200, 240, size=20, fill='black')

        
    elif app.infoScreen:
        drawRect(0, 0, 400, 400, fill='black')
        drawLabel('This is how to play Tetris! (112 edition)', 200, 50, size = 20, fill = 'pink', bold=True)
        drawLabel('''Press p to start the game.''', 200, 80, size = 16, fill = 'pink', bold=True)
        drawLabel('If you want to pause, press p again.', 200, 100, size = 16, fill = 'pink', bold=True)
        drawLabel('To rotate your pieces, press the arrow keys.', 200, 120, size = 16, fill = 'pink', bold=True)
        drawLabel('To hard drop a piece, press space.', 200, 140, size = 16, fill = 'pink', bold=True)
        drawLabel('A single line burn is worth 100 points.', 200, 180, size = 16, fill = 'pink', bold=True)
        drawLabel('A double line is worth 200, and so on.', 200, 200, size = 16, fill = 'pink', bold=True)
    
        drawLabel('Every 10 lines, your level increases and', 200, 220, size = 16, fill = 'pink', bold=True)
        drawLabel(' the game runs faster.', 200, 240, size = 16, fill = 'pink', bold=True)
        
        drawLabel('HAVE FUN!', 200, 280, size = 16, fill = 'pink', bold=True)
        drawLabel('Press esc to exit this screen.', 200, 300, size = 16, fill = 'pink', bold=True)

        
    else:
        drawLabel('TETRIS', 200, 40, align='center', size = 16)
        drawLabel(f'Score = {app.score}', 45, 250, size=16)
        drawLabel(f'Level = {app.level}', 45, 270, size=16)
        drawLabel(f'Lines = {app.lines}', 45, 290, size=16)
        drawLabel('Press i for information on how to play.',  200, 380, size = 12)
        drawBoard(app)
        drawPiece(app)
        drawBoardBorder(app)
    
def onKeyPress(app, key):
    if app.gameOver:
        restartGame(app)
        
    if key == 'left':  movePiece(app, 0, -1)
    elif key == 'right':  movePiece(app, 0, +1)
    elif key == 'up': rotatePieceClockwise(app)
    elif key == 'down':  movePiece(app, +1, 0)
    elif key == 'space': hardDropPiece(app)
    elif key == 's': takeStep(app)
    elif key == 'p': 
        app.paused = not app.paused
    elif key == 'i':
        if not app.paused:
            app.paused = True
        app.infoScreen = True
    elif key == 'escape':
        app.infoScreen = not app.infoScreen
        app.paused = False

def loadNextPiece(app):
    pieceIndex = random.randrange(len(app.tetrisPieces))
    if app.nextPieceIndex < len(app.tetrisPieces):
        loadPiece(app, app.nextPieceIndex)
        app.nextPieceIndex += 1
    else:
        app.nextPieceIndex = 0

      
def movePiece(app,drow,dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if pieceIsLegal(app):
        return True
    else:
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False

def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass

def pieceIsLegal(app):
    if app.piece is not None:
        for row in range(len(app.piece)):
            for col in range(len(app.piece[row])):
                if app.piece[row][col]:
                    boardRow = app.pieceTopRow + row
                    boardCol = app.pieceLeftCol + col
                    if boardRow < 0 or boardRow >= app.rows or boardCol <0 or boardCol >= app.cols:
                        return False
                    if app.board[boardRow][boardCol] is not None:
                        return False
                    
    return True #piece is good and in bounds

def onStep(app):
    if app.gameOver:
        return
    app.counter+=1
    if not app.paused:
        takeStep(app)
    else:
        return

def restartGame(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 80
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = 1
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    app.pieceTopRow = 0
    app.nextPieceIndex = 0
    loadNextPiece(app)
    pieceWidth = len(app.piece[0])
    boardWidth = app.cols
    app.pieceLeftCol = (boardWidth - pieceWidth)//2
    app.pieceColor = app.tetrisPieceColors[app.nextPieceIndex]
    app.paused = False
    app.stepsPerSecond = 1 #start mega slow like actual tetris
    app.counter = 0
    app.score = 0
    app.lines = 0
    app.level = 1
    app.gameOver = False
    app.infoScreen = False



def takeStep(app):
    if not movePiece(app, +1, 0):
    # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)
  
def pointScheme(app, fullPop):
    default = 100
    if fullPop < 4:
        return fullPop * default
    elif fullPop == 0:
        return

def levelScheme(app, lines):
    if app.lines %11 == 10:
        app.level += 1
    else:
        return

def removeFullRows(app):
    i=0
    fullPop = 0
    while i < len(app.board):
        j=0
        singlePop = 0
        while j < len(app.board[i]):
            if app.board[i][j] != None: 
                singlePop += 1 #pop if its none
            j += 1
            
        if singlePop == len(app.board[i]): #if you popped everything in that given row...
            fullPop += 1 #..then you popped the whole row
            app.board.pop(i)
        else: 
            i += 1
    app.score += pointScheme(app, fullPop) #give user score
    app.lines += fullPop #add on how many lines were popped 
    levels = levelScheme(app, app.lines)
    if levels is not None:
        app.level = levels
    
    emptyNewRows = [None] * len(app.board[0]) #initialize new list to be inserted
    for _ in range(fullPop):
        app.board.insert(0, list(emptyNewRows)) #list to avoid aliasing
    
                

def placePieceOnBoard(app):
    if app.piece is not None:
        for row in range(len(app.piece)):
            for col in range(len(app.piece[row])):
                if app.piece[row][col]:
                    boardRow = app.pieceTopRow + row
                    boardCol = app.pieceLeftCol + col
                    
                    app.board[boardRow][boardCol] = app.pieceColor

def drawPiece(app):
    if app.piece is not None:
        for row in range(len(app.piece)):
            for col in range(len(app.piece[row])):
                if app.piece[row][col]:
                    boardRow = app.pieceTopRow + row
                    boardCol = app.pieceLeftCol + col
                    drawCell(app, boardRow, boardCol, app.pieceColor)
                

def rotatePieceClockwise(app):
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    
    app.piece = rotate2dListClockwise(app.piece)
    
    oldRows = len(oldPiece)
    oldCols = len(oldPiece[0])
    newRows = len(app.piece)
    newCols = len(app.piece[0])
    
    centerRow = oldTopRow + oldRows//2 
    app.pieceTopRow = centerRow - newRows//2
    
    leftCol = oldLeftCol + oldCols//2
    app.pieceLeftCol = leftCol - newCols//2
    
    if pieceIsLegal(app):
        return True
    else: 
        app.piece = oldPiece
        app.pieceTopRow =  oldTopRow
        app.pieceLeftCol = oldLeftCol
        return False
    

def rotate2dListClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [[None for _ in range(newCols)] for _ in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newCol = oldRow 
            newRow = oldCol
            M[newRow][newCol] = L[oldRow][oldCol] 
    for index in range(len(M)):
        M[index] = M[index][::-1]

    return M

def loadPiece(app, pieceIndex):
    pieceIndex = random.randrange(len(app.tetrisPieces))
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceTopRow = 0
    pieceWidth = len(app.piece[0])
    boardWidth = app.cols
    app.pieceLeftCol = (boardWidth - pieceWidth)//2
    
    if not pieceIsLegal(app):
        app.gameOver = True

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def resizeBoard(app, numRows, numCols, boardSize):
    app.rows = numRows
    app.cols = numCols
    app.boardLeft, app.boardWidth, app.boardHeight = boardSize
    app.board = [([None] * app.cols) for row in range(app.rows)]





def main():
    runApp()

main()