from graphics import *
import threading

win_size = 400

def main():
	win = GraphWin("Gyro", win_size, win_size)
	# points = (
	# 	Point(win_size/4, win_size/4), 
	# 	Point(win_size*3/4, win_size/4),
	# 	Point(win_size*3/4, win_size*3/4),
	# 	Point(win_size/4, win_size*3/4)
	# 	)
	p = Polygon(
			Point(win_size/4, win_size/4), 
			Point(win_size*3/4, win_size/4),
			Point(win_size*3/4, win_size*3/4),
			Point(win_size/4, win_size*3/4)
			)
	p.draw(win)
	win.getMouse()
	win.close()


def g():
	# draw initial graphics to the screen
	win = GraphWin("Gyro", win_size, win_size)
	p = Polygon(
		Point(win_size/4, win_size/4), 
		Point(win_size*3/4, win_size/4),
		Point(win_size*3/4, win_size*3/4),
		Point(win_size/4, win_size*3/4)
		)
	p.draw(win)
	win.getMouse()

	win.close()


def main():
	gThread = threading.Thread(target=g)
	gThread.start()


main()