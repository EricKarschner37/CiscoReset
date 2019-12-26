import serial
import threading

ports = set()
error = False
def reply_to_with(com, target, message):
	global error
	while(True):
		line = com.read_until(target)
		if b'read only file system' in line or b'invalid' in line or b'Error' in line:
			error = True
		if target in line:
			if message == 'flash_init' + '\r':
				try:
					print("Press Enter to continue \n")
					raw_input()
				except EOFError:
					print("Continuing... \n")
			com.write(message.encode())
			break
	return

def reset_on_com(com):
	global ports

	reply_to_with(com, b'\rswitch: ', 'flash_init' + '\r')
	reply_to_with(com, b'\rswitch: ', 'del flash:config.text' + '\r')
	reply_to_with(com, b'(y/n)?', 'y' + '\r')
	reply_to_with(com, b'\rswitch: ', 'del flash:vlan.dat' + '\r')
	reply_to_with(com, b'(y/n)?', 'y' + '\r')
	reply_to_with(com, b'\rswitch: ', 'boot' + '\r')

	while(True):
		line = com.read_until(b'RETURN')
		if b'RETURN' in line:
			ports.remove(com.name[3:])
			if error: print("Something went wrong with the device at " + com.name)
			else: print("Device at " + com.name + " is reset.")
			break

while True:
	raw_input()
	print("Active: ")
	print([port for port in ports])
	portNum = str(input("What number COM port would you like to reset?\n"))
	ser = serial.Serial(
		port='COM' + portNum,
		baudrate=9600,
		parity="N",
		stopbits=1,
		xonxoff=False,
		bytesize=8,
		timeout=8
	)
	ports.add(portNum)
	thread = threading.Thread(target=reset_on_com, args=(ser,))
	thread.start()

