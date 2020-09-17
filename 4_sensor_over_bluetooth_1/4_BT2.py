import serial
import subprocess
import threading
import sys
from time import sleep


kill = False


def main():
	global ser
	global kill

	PORT = get_BT_port()
	if not PORT:
		print("No port found!")
		return
	ser = serial.Serial(PORT, 115200, timeout=1)
	print("Connected to ESP32. type 'q' to kill.")

	uiThread = threading.Thread(target=ui, daemon=True)
	uiThread.start()

	while not kill:
		# s = ser.read().decode()
		# if s == 'x':
		# 	a = ser.read()
		# 	b = ser.read()
		# 	print(a, b)

		s = ser.read().decode()
		if s:
			a = ser.read()
			b = ser.read()

			# https://stackoverflow.com/questions/49864293/python-byte-doesnt-print-binary
			aInt = int.from_bytes(a, byteorder=sys.byteorder)
			bInt = int.from_bytes(b, byteorder=sys.byteorder)

			# https://www.tutorialspoint.com/python/bitwise_operators_example.htm
			num = aInt << 8 | bInt

			print(num)

	ser.close()


def ui():
	global kill

	while not kill:
		if input() == 'q':
			print("killing...")
			kill = True

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