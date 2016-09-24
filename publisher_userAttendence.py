import time
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
 
SLEEPTIME =1
IP = "192.168.1.178"
 
def update(status = 0):
    publish.single("/user", status, hostname=IP)
 
# connection setting
button_pin = 17
 
userPresence = 0
userAbsence = 1
 
# setup input
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN)
 
# upload user presence every second.
def checkStatus():
    input_value = GPIO.input(button_pin)
    if input_value == False:
        update(userAbsence)
    else:
        update(userPresence)
 
while 1:
    checkStatus()
    time.sleep(SLEEPTIME)
