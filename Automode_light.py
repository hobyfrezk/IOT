import RPi.GPIO as GPIO
import time

#WIRING SETTING
LED = 4


USER_ABSENCE = 2
USER_PRESENCE = 1

# state class declaration
class state:
	def __init__(self, datatype, data):
		self.type = str(datatype)
		self.data = data
		self.timeout = 0
		
def update_data(data): # to be done(thingspeak)..
	

# used to control brightness of LED light
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
		time.sleep(5)

# we only care about neweast data, so read last number of file, furthermore, can be optimized by using json format data.
def read_data (filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])

# brighter the natural light, the darker of our LED.
def light_requirements():
    light = read_data("lightlog.txt")
    if light  <100:
        return 100
    if light  <1000:
        return 50
    if light  <2500:
        return 30
    if light  <4000:
        return 10
    else:
        return 0
	

if __main___ == "__main__":
	light_control() # light is turned off at begining
	absence_time = 0 # initialize absence counter
	user = State(datatype = "user", data = int(read_data("userlog.txt")))  # create user state instance
    
    try:
    	while True:
    		# if user absence, check the absence counter, if reaches 15 minutes, turn off the led
    		if user.data == USER_ABSENCE: 
    			if user.timeout < 900:
    				absence_time = user.timeout + 5
                    user.timeout = absence_time
                    time.sleep(5)
                    
                elif user.timeout  >= 900:
                light_control()
                absence_time= 0
                time.sleep(15)
 
                else:
                    print "Error in Sleep Mode"
                    time.sleep(999999)
			#if user presence, adjust the brightness from date of sensors
            elif user.data == USER_PRESENCE: 
                absence_time = 0
                control = light_requirements()
                light_control(control)
 
            else:
                print "Error in Reading Log File"
             
            data = int(read_data("userlog.txt"))
            user.data = data
			
    except KeyboardInterrupt:
    GPIO.cleanup()		
    		
    		
    		
    		
    		
    		
	
