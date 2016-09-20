import RPi.GPIO as GPIO
import time
from Automode_light import automode
 
LED = 4


USER_PRESENCE = 0
USER_ABSENCE = 1
AUTOMODE = 2
INTERACTIVE = 3

def light_control(requirement = 0):
    print requirement
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
     
    if requirement ==0: #turn off led
        GPIO.output(LED, 0)
         
    else: # control led brightness according to requirement
        portLED = GPIO.PWM(LED, 100)
        portLED.start(requirement)

        
        
def interactiveMode():
	print "Select mode:"
	print "1. go back to auto mode"
	print "2. select brightness"
	print "3. turn off the system"
	
	command = raw_input()
	if str(command) == str(1):
		automode()
		
	if str(command) == str(2):
		print "Enter the brightness you want"
		brightness = raw_iuput()
		light_control(brightness)
		
	
	
	
	
