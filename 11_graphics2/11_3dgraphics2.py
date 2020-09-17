# based on this tutorial for pygame and OpenGL: https://www.youtube.com/watch?v=R4n4NyDG2hI
# most of the BT implementation is taken from 9_data_on_request
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import serial
import subprocess
import sys


FRAME_RATE_CAP = 30
ANGLE_MULTIPLIER = 1

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


# defines a cube based on given vertices
# used by OpenGL to draw the cube
def Cube():
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()


# used to find the correct port to connect to
def get_BT_port():
	ports = subprocess.check_output(["ls /dev/*"], shell=True)
	ports = ports.decode("utf-8")
	ports_list = ports.split("\n")
	for port in ports_list:
		if port.find("ESP") != -1:
			return port
	return False


# used to combine the single bytes of data from ESP into a 16bit int
def combine_bytes(byte1, byte2):
	num1 = int.from_bytes(byte1, byteorder=sys.byteorder)
	num2 = int.from_bytes(byte2, byteorder=sys.byteorder)
	return num1 << 8 | num2


# asks the ESP for its current gyro data, outputs it as a list
def get_data():
	global ser
	output = []
	ser.write('1'.encode())
	for _ in range(3):
		byte1 = ser.read()
		byte2 = ser.read()
		num = combine_bytes(byte1, byte2)
		output.append(num)
	return output


def print_data(data):
	global axes
	for i in range(3):
		print(axes[i], "-", data[i])
	print("")


# rotates based on given angle values
def rotate(angles):
	glRotatef(angles[0], 1, 0, 0)
	glRotatef(angles[1], 0, 1, 0)
	glRotatef(angles[2], 0, 0, 1)


# updates the camera angle of the current fram with the correct angle data from ESP
def update_rotation():
	global previous_angles
	global ANGLE_MULTIPLIER

	rev = [-a for a in previous_angles]
	angles = [a * 360 / 2**16 for a in get_data()]
	angles = [a * ANGLE_MULTIPLIER for a in angles]
	print_data(angles)
	rotate(rev)
	rotate(angles)

	previous_angles = angles


def main():
	global ser
	# Pygame initialisation
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	# Bluetooth serial initialisation
	PORT = get_BT_port()
	if not PORT:
		print("No port found!")
		pygame.quit()
		quit()
	ser = serial.Serial(PORT, 115200, timeout=1)
	# OpenGL initialisation
	gluPerspective(45, display[0]/display[1], 0.1, 50.0)	# something with viewing angle
	glTranslatef(0.0, 0.0, -15.0)
	glRotatef(0, 0, 0, 0)

	# main loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				ser.close()
				quit()

		update_rotation()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Cube()
		pygame.display.flip()
		pygame.time.wait(int(1000/FRAME_RATE_CAP))


main()











