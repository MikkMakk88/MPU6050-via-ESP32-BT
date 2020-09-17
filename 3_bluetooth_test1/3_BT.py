import serial
import subprocess
import threading
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
	print("Connected to ESP32.")

	uiThread = threading.Thread(target=ui)
	uiThread.start()

	message = ""
	while not kill:
		s = ser.read().decode()

		if s:
			message += s
		elif message:
			print(message)
			message = ""

	ser.close()


def ui():
	global ser
	global kill

	while not kill:
		i = input()
		if i == "q":
			print("killing")
			kill = True		
		else:
			ser.write(i.encode())

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