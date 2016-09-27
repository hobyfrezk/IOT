import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import smbus
from smbus import SMBus
import RPi.GPIO as GPIO


#parameter setting
TIMESLEEP = 1
#IP = "169.254.205.192"
IP = "192.168.1.178"
userAbsence = 0
userPresence = 1
AUTOMODE = 2
INTERACTIVEMODE = 3
COUNTER = 0

# connection setting
button_pin_user = 17
button_pin_mode  = 22

# setup input
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin_user, GPIO.IN)
GPIO.setup(button_pin_mode, GPIO.IN)


TSL2561 = SMBus(1)
address = 0x39
control_on = 0x03
control_off = 0x00

def enable():
    TSL2561.write_byte(address, 0x80)
    TSL2561.write_byte(address, control_on)

def checkLight():
    enable()
    var = [5, 5, 5, 5]
    var = TSL2561.read_i2c_block_data(0x39, 0x8C)
    payloadlight = ((var[1]<<8) + var[0])
    publish.single("/light", payloadlight , qos=1, retain=True, hostname=IP)
    
def checkUser():
    input_value = GPIO.input(button_pin_user)
    if input_value == False:
        publish.single("/user", userAbsence, hostname=IP)
    else:
        publish.single("/user", userPresence, hostname=IP)

def checkMode():
    global COUNTER
    input_value = GPIO.input(button_pin_mode)
    # when button pressed, remember this action and switch mode state
    if input_value == False:
        COUNTER = COUNTER+1
    else:
        pass
    
    if COUNTER%2 != 0:
        publish.single("/mode", INTERACTIVEMODE, hostname=IP)
    else:
        publish.single("/mode", AUTOMODE, hostname=IP)

while True:
    checkLight()
    checkUser()
    checkMode()
    time.sleep(1)




