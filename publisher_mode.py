import time
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
 
COUNTER = 0
SLEEPTIME = 1
IP = "192.168.1.178"
 
AUTOMODE = 2
INTERACTIVEMODE = 3
 
def update(status = 0):
    publish.single("/mode", status, hostname=IP)
 
# connection setting
button_pin = 22
 
 
# setup input
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN)
 
# upload user presence every second. system start with AUTOMODE
def checkMode():
    global COUNTER
     
    input_value = GPIO.input(button_pin)
 
    # when button pressed, remember this action and switch mode state
    if input_value == False:
        COUNTER = COUNTER+1
    else:
        pass
     
    if COUNTER%2 != 0:
        return  INTERACTIVEMODE
    else:
        return AUTOMODE
         
while True:
    update(checkMode())
    time.sleep(SLEEPTIME)
