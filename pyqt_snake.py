#!/usr/bin/python
import sys
from random import randrange
from PyQt5 import QtWidgets, QtCore, QtGui

# Initialize a new Qt Widget
class Snake(QtWidgets.QWidget):
	def __init__(self):
        # Inherit the features of QWidget class
		super(Snake, self).__init__()
        # Print the window
		self.initUI()

	def initUI(self):
		self.highscore = 0
		self.newGame()
        # Define the window background in hexadecimal
		self.setStyleSheet("QWidget { background: #A9F5D0 }")
		self.setFixedSize(300, 300)
		self.setWindowTitle('Snake')
		self.show()

	# The custom timer repaint all the objects in the window
    #  defined in newGame method
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.direction(self.lastKeyPress)
			self.repaint()
		else:
			QtWidgets.QFrame.timerEvent(self, event)

    # Executed at every milliseconds of the timer
	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
        # Print the score board
		self.scoreBoard(qp)
        # Put the food
		self.placeFood(qp)
        # Draw the snake
		self.drawSnake(qp)
        # Print an updated score
		self.scoreText(event, qp)
        # If game is over
		if self.isOver:
			self.gameOver(event, qp)
		qp.end()

    # Executed when there is a key press
	def keyPressEvent(self, e):
		if not self.isPaused:
            # To avoid that the snake go backwards, we check the previous button
			if e.key() == QtCore.Qt.Key_Up and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
				self.direction("UP")
				self.lastKeyPress = 'UP'
			elif e.key() == QtCore.Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
				self.direction("DOWN")
				self.lastKeyPress = 'DOWN'
			elif e.key() == QtCore.Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
				self.direction("LEFT")
				self.lastKeyPress = 'LEFT'
			elif e.key() == QtCore.Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
				self.direction("RIGHT")
				self.lastKeyPress = 'RIGHT'
            # Take a break!
			elif e.key() == QtCore.Qt.Key_P:
				self.pause()
        # The game is paused let's start
		elif e.key() == QtCore.Qt.Key_P:
			self.start()
		elif e.key() == QtCore.Qt.Key_Space:
			self.newGame()
		elif e.key() == QtCore.Qt.Key_Escape:
			self.close()

    # Define the various variables
	def newGame(self):
        # Default score
		self.score = 0
        # Initial snake position
		self.x = 12;
		self.y = 36;
		self.snakeArray = [[self.x, self.y], [self.x-12, self.y], [self.x-24, self.y]]
        # Define a first fake key press
		self.lastKeyPress = 'RIGHT'
		self.timer = QtCore.QBasicTimer()
        # Initial fake position for food
		self.foodx = 0
		self.foody = 0
        # Status of the game
		self.isPaused = False
		self.isOver = False
		self.FoodPlaced = False
        # The timer is executed every 100ms
		self.speed = 100
		self.start()

	def start(self):
		self.isPaused = False
        # Set the timer
		self.timer.start(self.speed, self)
        # Let's do a repaint of the window
		self.update()
        
	def pause(self):
		self.isPaused = True
        # We stop the time progressing
		self.timer.stop()
        # Let's do a repaint of the window
		self.update()

	def checkStatus(self, x, y):
        # Check of the position of the snake is at the borders
		pos = y > 288 or x > 288 or x < 0 or y < 24
        # If the snake touched the borders or the window is full
		if pos or (self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]):
			self.pause()
			self.isPaused = True
			self.isOver = True
			return False
        # If the snake is at the same position of the food
		elif self.y == self.foody and self.x == self.foodx:
			self.FoodPlaced = False
			self.score += 1
			return True
        # Remove the last piece of the snake
		self.snakeArray.pop()
		return True

	def direction(self, dir):
        # Change the direction of the snake 
        # Calculate the next pixel where will be
		if (dir == "DOWN" and self.checkStatus(self.x, self.y+12)):
			self.y += 12
		elif (dir == "UP" and self.checkStatus(self.x, self.y-12)):
			self.y -= 12
		elif (dir == "RIGHT" and self.checkStatus(self.x+12, self.y)):
			self.x += 12
		elif (dir == "LEFT" and self.checkStatus(self.x-12, self.y)):
			self.x -= 12
        # Refresh the window
		self.repaint()
        # Save in memory the new snake position
		self.snakeArray.insert(0 ,[self.x, self.y])

	# Places the food when theres none on the board
	def placeFood(self, qp):
		if self.FoodPlaced == False:
			self.foodx = randrange(24)*12
			self.foody = randrange(2, 24)*12
            # IF the new position is not where is the snake
			if not [self.foodx, self.foody] in self.snakeArray:
				self.FoodPlaced = True;
        # Draw the food and set the color
		qp.setBrush(QtGui.QColor(80, 180, 0, 160))
		qp.drawRect(self.foodx, self.foody, 12, 12)

	# Draws each piece of the snake
	def drawSnake(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
        # Draw the piece and set the color
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		for i in self.snakeArray:
            # For every piece position draw it
			qp.drawRect(i[0], i[1], 12, 12)

	def scoreBoard(self, qp):
        # Design the board
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(25, 80, 0, 160))
		qp.drawRect(0, 0, 300, 24)

	def scoreText(self, event, qp):
		qp.setPen(QtGui.QColor(255, 255, 255))
		qp.setFont(QtGui.QFont('Decorative', 10))
        # The first 2 numers are the pixel position for the text
        #  We need to convert the score as string to print it
		qp.drawText(8, 17, "SCORE: " + str(self.score))
		qp.drawText(200, 17, "HIGHSCORE: " + str(self.highscore))

	def gameOver(self, event, qp):
        # Compare the actual score with the maximum and get it
		self.highscore = max(self.highscore, self.score)
		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "GAME OVER")
		qp.setFont(QtGui.QFont('Decorative', 8))
		qp.drawText(90, 170, "press space to play again")

# Classic way to execute a python class
def main():
    # Create a new QT app empty
	app = QtWidgets.QApplication(sys.argv)
    # Run on this app our class
	ex = Snake()
    # If the window is trying to getting closed kill the app
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
