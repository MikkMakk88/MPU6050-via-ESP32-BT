import serial
import subprocess
import threading
import sys
from time import sleep


kill = False
axes = ('x', 'y', 'z')


def main():
	global ser
	global kill

	PORT = get_BT_port()
	if not PORT:
		print("No port found!")
		return
	ser = serial.Serial(PORT, 115200, timeout=1)
	print("Connected to ESP32.")

	uiThread = threading.Thread(target=ui, daemon=True)
	uiThread.start()

	while not kill:
		if ser.in_waiting >= 6:
			data = get_data()
			print_data(data)
	ser.close()


def ui():
	global kill
	global ser
	while not kill:
		i = input()
		if i == 'q':
			print("Killing...")
			kill = True
		elif i == '':
			ser.write('1'.encode())


def print_data(data):
	global axes
	for i in range(3):
		print(axes[i], "-", data[i])
	print("")


def get_data():
	global axes
	output = []
	for axis in axes:
		byte1 = ser.read()
		byte2 = ser.read()
		num = combine_bytes(byte1, byte2)
		output.append(num)
	return output


def combine_bytes(byte1, byte2):
	num1 = int.from_bytes(byte1, byteorder=sys.byteorder)
	num2 = int.from_bytes(byte2, byteorder=sys.byteorder)
	return num1 << 8 | num2


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