import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import time
from rtmidi.midiutil import open_midiinput

previous_angles = [0, 0, 0]
axes = ('x', 'y', 'z')
vertices = (
	(3, -3, -1),
	(3, 3, -1),
	(-3, 3, -1),
	(-3, -3, -1),
	(3, -3, 1),
	(3, 3, 1),
	(-3, -3, 1),
	(-3, 3, 1)
	)
edges = (
	(0, 1),
	(0, 3),
	(0, 4),
	(2, 1),
	(2, 3),
	(2, 7),
	(6, 3),
	(6, 4),
	(6, 7),
	(5, 1),
	(5, 4),
	(5, 7)
	)

FRAME_RATE_CAP = 30


# callback handler for rtmidi in
class MidiInputHandler(object):
	values = [0, 0 , 0]		# x, y, z

	def __init__(self, port):
		self.port = port

	def __call__(self, event, data=None):
		message, *_ = event
		axis = message[1] - 17
		val = message[2]
		MidiInputHandler.values[axis] = val
		print(MidiInputHandler.values)


# defines a cube based on given vertices
# used by OpenGL to draw the cube
def Cube():
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()


# rotates based on given angle values
def rotate(angles, rev=False):
	if rev:
		angles = [-a for a in angles]
		glRotatef(angles[2], 0, 0, 1)
		glRotatef(angles[1], 0, 1, 0)
		glRotatef(angles[0], 1, 0, 0)
	else:
		glRotatef(angles[0], 1, 0, 0)
		glRotatef(angles[1], 0, 1, 0)
		glRotatef(angles[2], 0, 0, 1)


# updates the camera angle of the current fram with the correct angle data from ESP
def update_rotation():
	global previous_angles

	rotate(previous_angles, rev=True)

	angles = [a * 360 / 2**7 for a in MidiInputHandler.values]
	rotate(angles)

	previous_angles = angles


def main():
	# rtmidi inisialisation
	port = 1
	midiin, port_name = open_midiinput(port)
	midiin.set_callback(MidiInputHandler(port_name))
	# Pygame initialisation
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	# OpenGL initialisation
	gluPerspective(45, display[0]/display[1], 0.1, 50.0)	# FOV, viewing angle, clipping distance
	glTranslatef(0.0, 0.0, -15.0)
	glRotatef(0, 0, 0, 0)

	# main loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				midiin.close_port()
				del midiin
				quit()

		update_rotation()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Cube()
		pygame.display.flip()
		pygame.time.wait(int(1000/FRAME_RATE_CAP))


main()