import graphics as g
import serial
import subprocess
import threading
import sys
from time import sleep


win_size = 400
kill = False
axes = {
	'00': 'x',
	'01': 'y',
	'10': 'z',
	'11': 'e'
}


def main():
	global ser
	global kill

	# get port to connect to ESP
	PORT = get_BT_port()
	if not PORT:
		print("No port found!")
		return
	ser = serial.Serial(PORT, 115200, timeout=1)
	print("Connected to ESP32. Hit Enter to kill.")

	# multithreading seems to not behave very nicely with tkinter(which is what graphics is based on)
	# commenting this out for now but could be fixed later
	# 	https://stackoverflow.com/questions/51729665/threads-and-tkinter-not-working-together
	# 	https://wiki.tcl-lang.org/page/Tcl+event+loop
	# start the ui thread for manual killing
	# uiThread = threading.Thread(target=ui, daemon=True)
	# uiThread.start()

	# win = g.GraphWin("Gyro", win_size, win_size)
	# win.setBackground("#000000")

	# p = g.Polygon(
	# 	g.Point(win_size/4, win_size/4), 
	# 	g.Point(win_size*3/4, win_size/4),
	# 	g.Point(win_size*3/4, win_size*3/4),
	# 	g.Point(win_size/4, win_size*3/4)
	# 	)
	# p.setWidth(3)
	# p.setOutline("#ffffff")
	# p.setFill("#757575")
	# p.draw(win)

	# start communication with the ESP and start main loop
	while not kill:
		byte1 = ser.read()
		if byte1:
			byte2 = ser.read()

			result = ReadGyroValue(byte1, byte2)
			print(result)
		else:
			ser.write('1'.encode())
		sleep(1/1000)

	# once loop is killed we close communication with ESP,
	# close graphics window and exit the main function
	ser.close()
	# win.close()


# function targeted by thread for manual killing of program
def ui():
	global kill
	input()
	print("Killing...")
	kill = True


def getPoints(GyX, GyY, GyZ):
	# takes in the values from the gyro and outputs points of the rectangle to be drawn
	pass


# function to return data from raw bytes sent over serial
def ReadGyroValue(byte1, byte2):
	# decodes an incoming 16bit number and returns a tuple containing the value and axis of gyro reading
	Int1 = int.from_bytes(byte1, byteorder=sys.byteorder)
	Int2 = int.from_bytes(byte2, byteorder=sys.byteorder)

	Bin1 = "{0:08b}".format(Int1)
	Bin2 = "{0:08b}".format(Int2)
	
	axis = axes[Bin1[:2]]

	# truncate the first 2 bits (0x3F = 00111111)
	Int1 = Int1 & 0x3F 
	# then shift over int1 into the MSB and bin-or it with Int2
	val = (Int1 << (2 + 8)) | (Int2 << 2)

	return (axis, val)
	# return("int:", val, ", bin:", Bin1+Bin2)


# function that returns the COM port for the ESP
def get_BT_port():
	ports = subprocess.check_output(["ls /dev/*"], shell=True)
	ports = ports.decode("utf-8")
	ports_list = ports.split("\n")
	for port in ports_list:
		if port.find("ESP") != -1:
			return port
	return False


if __name__ == "__main__":
	main()