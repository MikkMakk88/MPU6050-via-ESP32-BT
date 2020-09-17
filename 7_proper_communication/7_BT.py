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
	print("Connected to ESP32. Hit Enter to kill.")

	uiThread = threading.Thread(target=ui, daemon=True)
	uiThread.start()

	ser.write('1'.encode())
	while not kill:
		if ser.in_waiting:
			axis = ser.read().decode()
			i = ser.read()
			j = ser.read()

			# https://stackoverflow.com/questions/49864293/python-byte-doesnt-print-binary
			iInt = int.from_bytes(i, byteorder=sys.byteorder)
			jInt = int.from_bytes(j, byteorder=sys.byteorder)

			# https://www.tutorialspoint.com/python/bitwise_operators_example.htm
			num = iInt << 8 | jInt

			data = (axis, num)

			print(data)
			if axis == "z":
				print("")

	ser.write('0'.encode())
	ser.close()


def ui():
	global kill

	input()

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