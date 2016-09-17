# used to read log file in local, we only care about neweast data, so read last number of file
def read_data(filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])
    
def light_control(requirement = 0):
	GPIO.setwarings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED, GPIO.OUT)
	
	if requirement == 0:
		GPIO.output(LED, 0)
	else:
		# use GPIO.PWM to countrol led brightness, and **sleep 5 seconds**.
		port4 = GPIO.PWM(LED, 100)
		port4.start (requirement)


# interactive mode
# ***sleep mode***
# ***adjustment brightness***
# ***go back to auto mode***
# ***turn off system***
def interactiveMode():
	print "Select mode:"
	print "1. go back to auto mode"
	print "2. select brightness"
	print "3. turn off the system"
	
	command = raw_input()
	if str(command) == str(1):
		
		
	
	if str(command) == str(2):
		
	
	
	if str(command) == str(3):
		
	
	
	
	

	
