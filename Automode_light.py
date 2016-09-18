import RPi.GPIO as GPIO
import datetime
import update from thingspeak

#WIRING SETTING
LED = 4


USER_ABSENCE = 2
USER_PRESENCE = 1

# state class declaration
class state:
	def __init__(self, datatype, data):
		self.type = str(datatype)
		self.data = data
		self.time = datetime.datetime.now()
		


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

def automode():
	user = State(datatype = "user", data = int(read_data("userlog.txt")))  # create user state instance
	time = 0
	
	if user.data == USER_ABSENCE:
		if time = 0:
			1st_absence_time = datetime.datetime.now()
		if (datetime.datetime.now() - 1st_absence_time).totalseconds() < 900:
			pass
		if (datetime.datetime.now() - 1st_absence_time).totalseconds() > 900:
			light_control()
		else:
            print "Error in Sleep Mode"
    
	elif user.data == USER_PRESENCE: 
        time = 0
        control = light_requirements()
        light_control(control)
	
    else:
        print "Error in Reading Log File"
	
