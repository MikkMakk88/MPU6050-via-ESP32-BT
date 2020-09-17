import serial
import subprocess
import threading
import sys
from time import sleep


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
		byte1 = ser.read()
		if byte1:
			byte2 = ser.read()

			result = ReadGyroValue(byte1, byte2)
			print(result)
		# if byte1:
		# 	Int1 = int.from_bytes(byte1, byteorder=sys.byteorder)
		# 	Bin1 = "{0:08b}".format(Int1)
		# 	print(Bin1)


	ser.write('0'.encode())
	ser.close()


def ui():
	global kill
	input()
	print("Killing...")
	kill = True


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