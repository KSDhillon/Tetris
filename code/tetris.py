from Tkinter import *
import random

CELL_SIZE = 30
MARGIN = 50
TOP_MARGIN = 60
DROP_DELAY = 700 #ms


def run(row=15,col=10):
	root = Tk()
	winWidth = CELL_SIZE*col + 2*MARGIN
	winHeight = CELL_SIZE*row + MARGIN + TOP_MARGIN
	global canvas	
	canvas = Canvas(root, width = winWidth, height = winHeight)
	canvas.pack()
	root.resizable(width=0, height=0)
	class Struct: pass
	canvas.data = Struct()
	canvas.data.IsGameOver = False
	canvas.data.row = row
	canvas.data.col = col
	canvas.data.winWidth = winWidth
	canvas.data.winHeight =  winHeight
	root.bind("<Key>", keyPressed)
	init()
	newFallingPiece()
	newGhostPiece()
	timerFired()
	root.mainloop()

def init():
	board =  []
	score = 0
	canvas.data.score = score
	emptyColor = PhotoImage(file = "bg.gif")
	canvas.data.emptyColor = emptyColor
	for row in range(0,canvas.data.row):
		boardcol = []
		for col in range(0,canvas.data.col):
			boardcol.append(emptyColor)
		board.append(boardcol)
	iPiece = [
		[ True,  True,  True,  True]
	]
  	jPiece = [
		[ True, False, False ],
		[ True, True,  True]
	]
	lPiece = [
		[ False, False, True],
		[ True,  True,  True]
	]
	oPiece = [
		[ True, True],
		[ True, True]
	]
	sPiece = [
		[ False, True, True],
		[ True,  True, False ]
	]
	tPiece = [
		[ False, True, False ],
		[ True,  True, True]
	]
	zPiece = [
		[ True,  True, False ],
		[ False, True, True]
	]
	red = PhotoImage(file = "red.gif")
	yellow = PhotoImage(file = "yellow.gif")
	magenta = PhotoImage(file ="magenta.gif")
	pink = PhotoImage(file = "pink.gif")
	cyan = PhotoImage(file = "cyan.gif")
	green = PhotoImage(file = "green.gif")
	orange = PhotoImage(file = "orange.gif")
	tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
	tetrisPieceColors = [red, yellow, magenta, pink, cyan, green, orange]
	canvas.data.board = board
	canvas.data.emptyColor = emptyColor
	canvas.data.tetrisPieces = tetrisPieces
	canvas.data.tetrisPieceColors = tetrisPieceColors

def keyPressed(event):
	if canvas.data.IsGameOver == False:
		if event.keysym == "Left":
			moveFallingPiece(0,-1)
		if event.keysym == "Right":
			moveFallingPiece(0,1)
		if event.keysym == "q":
			rotateFallingPiece()
		if event.keysym == "e":
			rotateFallingPiece()
			rotateFallingPiece()
			rotateFallingPiece()		
		if event.keysym == "Down":
			moveFallingPiece(1,0)
		if event.keysym == "space":
			while moveFallingPiece(1,0):
				moveFallingPiece(1,0)
			placeFallingPiece()

		drawGame()
	if event.keysym == "r":
		init()
		newFallingPiece()
		if canvas.data.IsGameOver:
			timerFired()
		canvas.data.IsGameOver = False
		drawGame()

def drawGame():
	canvas.delete("all")
	canvas.create_rectangle(0,
							0,
							canvas.data.winWidth,
							canvas.data.winHeight, 
							fill = "Orange",
							state = HIDDEN)
	drawBoard()
	drawscore()
	drawInstructions()
	if canvas.data.IsGameOver == False:
		newGhostPiece()
		drawGhostPiece()
		drawFallingPiece()
	else:
		newGhostPiece()
		drawGhostPiece()
		drawFallingPiece()
		canvas.create_rectangle(canvas.data.winWidth/4, 
								canvas.data.winHeight/2 - 10,
								(3 * canvas.data.winWidth)/4,
								canvas.data.winHeight/2 + 10,
								fill = "White")
		canvas.create_text(canvas.data.winWidth/2,canvas.data.winHeight/2, text = "GAME OVER PRESS 'r' to RESTART")



def drawBoard():
	for row in range(0,canvas.data.row):
		for col in range(0,canvas.data.col):
			color = canvas.data.board[row][col]
			drawCell(row, col, color)

def drawCell(row,col,color):
	#outer rectangle
	canvas.create_rectangle(MARGIN + col * CELL_SIZE, 
							TOP_MARGIN + row * CELL_SIZE, 
							MARGIN + 1 + (1+col) * CELL_SIZE, 
							TOP_MARGIN + 1 + (1+row) * CELL_SIZE, 
							fill = "White")
	canvas.create_image(MARGIN + 1 + col * CELL_SIZE,
						TOP_MARGIN + 1 + row * CELL_SIZE,
						anchor = NW,
						image = color)
	#inner reactangle
'''	canvas.create_rectangle(MARGIN + 1 + col * CELL_SIZE, 
							MARGIN + 1 + row * CELL_SIZE, 
							MARGIN + (1+col) * CELL_SIZE, 
							MARGIN + (1+row) * CELL_SIZE, 
							fill = color)'''



def newFallingPiece():
	pieceIndex = random.randint(0,6)
	fallingPiece = canvas.data.tetrisPieces[pieceIndex]
	fallingPieceColor = canvas.data.tetrisPieceColors[pieceIndex]
	canvas.data.fallingPieceColor = fallingPieceColor
	canvas.data.fallingPiece = fallingPiece
	fallingPieceRow = 0
	fallingPieceCol = (canvas.data.col/2)
	fallingPieceCol -= len(fallingPiece[0])/2
	canvas.data.fallingPieceRow = fallingPieceRow
	canvas.data.fallingPieceCol = fallingPieceCol

def newGhostPiece():
	ghostpiece = canvas.data.fallingPiece
	ghostpiecerow = canvas.data.fallingPieceRow
	ghostpiececol = canvas.data.fallingPieceCol
	ghostpiececolor = PhotoImage(file = "gb.gif")
	canvas.data.ghostpiece = ghostpiece
	canvas.data.ghostpiecerow = ghostpiecerow
	canvas.data.ghostpiececol = ghostpiececol
	canvas.data.ghostpiececolor = ghostpiececolor

def drawFallingPiece():
	for row in range(0, len(canvas.data.fallingPiece)):
		for col in range(0, len(canvas.data.fallingPiece[0])):
			if canvas.data.fallingPiece[row][col] == True:
				drawCell(canvas.data.fallingPieceRow + row,
						canvas.data.fallingPieceCol + col,
						canvas.data.fallingPieceColor)

def drawGhostPiece():
	while (moveGhostPiece(1,0) == True):
		moveGhostPiece(1,0)
	for row in range(0, len(canvas.data.ghostpiece)):
		for col in range(0, len(canvas.data.ghostpiece[0])):
			if canvas.data.ghostpiece[row][col] == True:
				drawCell(canvas.data.ghostpiecerow + row,
						canvas.data.ghostpiececol + col,
						canvas.data.ghostpiececolor)				



def moveGhostPiece(drow, dcol):
	canvas.data.ghostpiecerow += drow
	canvas.data.ghostpiececol += dcol
	if (ghostPieceIsLegal() == False):
		canvas.data.ghostpiecerow -= drow
		canvas.data.ghostpiececol -= dcol
		return False
	return True



def moveFallingPiece(drow, dcol):
	canvas.data.fallingPieceRow += drow
	canvas.data.fallingPieceCol += dcol
	if (fallingPieceIsLegal() == False):
		canvas.data.fallingPieceRow -= drow
		canvas.data.fallingPieceCol -= dcol
		return False
	return True

def ghostPieceIsLegal():
	for row in range(0, len(canvas.data.ghostpiece)):
		for col in range(0, len(canvas.data.ghostpiece[0])):
			if canvas.data.ghostpiece[row][col] == True:
				if (canvas.data.ghostpiecerow < 0) or (canvas.data.ghostpiecerow + len(canvas.data.ghostpiece) > canvas.data.row):
					return False
				if (canvas.data.ghostpiececol < 0) or (canvas.data.ghostpiececol + len(canvas.data.ghostpiece[0]) > canvas.data.col):
					return False
				if (canvas.data.board[canvas.data.ghostpiecerow + row][canvas.data.ghostpiececol + col] != canvas.data.emptyColor):
					return False
	return True

def rotateFallingPiece():
	originCords = (canvas.data.fallingPieceRow, canvas.data.fallingPieceCol)
	orginPiece = canvas.data.fallingPiece
	canvas.data.fallingPieceCol += (len(canvas.data.fallingPiece[0])-len(canvas.data.fallingPiece))/2
	canvas.data.fallingPieceRow += (len(canvas.data.fallingPiece)-len(canvas.data.fallingPiece[0]))/2
	if (len(canvas.data.fallingPiece)-len(canvas.data.fallingPiece[0]))/2 < 0:
		canvas.data.fallingPieceRow += 1
	if (len(canvas.data.fallingPiece[0])-len(canvas.data.fallingPiece))/2 < 0:
		canvas.data.fallingPieceCol += 1
	'''if (len(canvas.data.fallingPiece[0]) == 4): # code to correct rotation for iPiece (to how real tetris has it)
		canvas.data.fallingPieceCol += 1
	if (len(canvas.data.fallingPiece) == 4):    # code to correct rotation for iPiece
		canvas.data.fallingPieceCol -= 1'''
	canvas.data.fallingPiece = zip(*canvas.data.fallingPiece)[::-1]
	if  fallingPieceIsLegal() == False:
		canvas.data.fallingPieceRow = originCords[0]
		canvas.data.fallingPieceCol = originCords[1]
		canvas.data.fallingPiece = orginPiece

def fallingPieceIsLegal():
	for row in range(0, len(canvas.data.fallingPiece)):
		for col in range(0, len(canvas.data.fallingPiece[0])):
			if canvas.data.fallingPiece[row][col] == True:
				if (canvas.data.fallingPieceRow < 0) or (canvas.data.fallingPieceRow + len(canvas.data.fallingPiece) > canvas.data.row):
					return False
				if (canvas.data.fallingPieceCol < 0) or (canvas.data.fallingPieceCol + len(canvas.data.fallingPiece[0]) > canvas.data.col):
					return False
				if (canvas.data.board[canvas.data.fallingPieceRow + row][canvas.data.fallingPieceCol + col] != canvas.data.emptyColor):
					return False
	return True

def timerFired():
	if moveFallingPiece(1,0) == False:
		placeFallingPiece()
		removeFullRow()
		newFallingPiece()
		newGhostPiece()
		if fallingPieceIsLegal() == False:
			canvas.data.IsGameOver = True
			drawGame()
			return
	drawGame()
	canvas.after(DROP_DELAY, timerFired)

def placeFallingPiece():
	for row in range(0, len(canvas.data.fallingPiece)):
		for col in range(0, len(canvas.data.fallingPiece[0])):
			if canvas.data.fallingPiece[row][col] == True:
				canvas.data.board[canvas.data.fallingPieceRow + row][canvas.data.fallingPieceCol + col] = canvas.data.fallingPieceColor

def removeFullRow():
	oldRow = len(canvas.data.board) - 1
	newRow = len(canvas.data.board) - 1
	fullRows = 0
	while newRow >= 0:
		if oldRow < 0:
			emptyRow =[]
			for idx in range(0,len(canvas.data.board[0])):
				emptyRow.append(canvas.data.emptyColor)
			canvas.data.board[newRow] = emptyRow
			newRow -= 1
		elif canvas.data.board[oldRow].count(canvas.data.emptyColor) != 0:
			rowVal = []
			for val in canvas.data.board[oldRow]:
				rowVal.append(val)
			canvas.data.board[newRow] = rowVal
			newRow -= 1
		else:
			fullRows +=1
		oldRow -= 1
	canvas.data.score += fullRows**2

def drawscore():
	canvas.create_text(10,10, anchor = NW, text = "Score: %d" % (canvas.data.score))

def drawInstructions():
	canvas.create_rectangle(165,8,370,53, fill = "Gray")
	canvas.create_text(170,10, anchor = NW, text = "ROTATE PIECE ANTI-CLOCKWISE: 'q'")
	canvas.create_text(170,23, anchor = NW, text = "ROTATE PIECE CLOCKWISE: 'e'")
	canvas.create_text(170,36, anchor = NW, text = "HARD DROP: 'spacebar'")



run()
