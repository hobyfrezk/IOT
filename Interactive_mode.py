import RPi.GPIO as GPIO
import time
from Automode_light import automode
 
LED = 4

def light_control(requirement = 0):
    print requirement
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
     
    if requirement ==0: #turn off led
        GPIO.output(LED, 0)
         
    else: # control led brightness according to requirement
        port4 = GPIO.PWM(LED, 100)
        port4.start(requirement)

        
        
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
		
	if str(command) == str(3):
	
	
	
