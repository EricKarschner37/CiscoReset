import serial
import threading

coms = dict()
error = False
def reply_to_with(com, target, message):
	global error
	while(True):
		line = com.read_until(target)
		if b'read only file system' in line or b'invalid' in line or b'Error' in line:
	    	    error = True
		if target in line:
	     	    if message == 'flash_init' + '\r':
			raw_input("Press Enter to continue \n")
		    com.write(message.encode())
    	            break
	return

def reset_on_com(com):
	reply_to_with(com, b'(y/n)?', 'y' + '\r')
	reply_to_with(com, b'\rswitch: ', 'del flash:vlan.dat' + '\r')
	reply_to_with(com, b'(y/n)?', 'y' + '\r')
	reply_to_with(com, b'\rswitch: ', 'boot' + '\r')

	while(True):
		line = com.read_until(b'RETURN')
		if b'RETURN' in line:
			if error: print("Something went wrong with the device at " + com.name)
			else: print("Device at " + com.name + " is reset.")
			break

def add_device():
    port_num = str(raw_input("What number COM port would you like to reset?\n"))
    ser = initialize_port(port_num)
    thread = threading.Thread(target=reset_on_com, args=(ser,))
    coms[port_num] = ser 
    thread.start()

def initialize_port(port_num):
    ser = serial.Serial(
           port='COM' + port_num,
           baudrate=9600,
           parity='N',
           stopbits=1,
           xonxoff=False,
           bytesize=8,
           timeout=8
         )
    reply_to_with(ser, b'\rswitch: ', 'flash_init' + '\r')
    return ser

def remove_device():
    port_num = str(raw_input("What number COM port would you like to end?\n"))
    com = coms[port_num]
    com.close()
    del coms[port_num]

def show_devices():
    print(coms.keys())

while True:
    command = raw_input("What would you like to do?\n").lower()
    if command == 'add' or command == 'start':
        add_device()
    elif command == 'end':
        remove_device()
    elif command == 'show' or command == 'active':
        show_devices()
