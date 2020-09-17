# a simple script that demonstrates how to interface with midi
# controllers

import time

from rtmidi.midiutil import open_midiinput


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


port = 1

midiin, port_name = open_midiinput(port)

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press ctrl-c to exit.")

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("")
finally:
	print("Killing...")
	midiin.close_port()
	del midiin