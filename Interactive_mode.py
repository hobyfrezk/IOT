import RPi.GPIO as GPIO
import time
 
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
        time.sleep(5)
        
if __name__ == "__main__":
	print "what mode do you want:"
	
