import RPi.GPIO as GPIO
import time,datetime
from thingspeak import update
 
 
USER_PRESENCE = 0
USER_ABSENCE = 1
AUTOMODE = 2
INTERACTIVEMODE = 3
 
 
 
# used to read local data
def read_data (filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])
 
def update2thgspk(user_behavior,led_brightness):
    update("USER", user_behavior)
    update("LED", led_brightness)
 
     
# countrol led brightness, close led by default
def light_control(requirement = 0):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
     
    if requirement == 0:
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        pass # all led have already been turned off at begining of this function
     
    if requirement == 1:
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
         
    if requirement == 2:
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
         
         
    if requirement == 3:
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(21,GPIO.LOW)
         
    if requirement ==4:
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(21,GPIO.HIGH)
         
 
 
 
# the function set how light the led should be, darker outside, brighter led.
def light_requirements():
    light = read_data("lightlog.txt")
    if light  <100:
        return 4
    if light< 1000:
        return 3
    if light  <2500:
        return 2
    if light  <4000:
        return 1
    else:
        return 0
 
def ControlMode():
    return read_data("modelog.txt")
 
     
def interactiveMode():
    global user_behavior, led_brightness
     
    print "Interactive mode:"
    print "1. go back to auto mode, push the button  then ENTER 1."
    print "2. Select brightness"
     
    command = raw_input()
    if str(command) == str(1):
        autoMode()
         
    if str(command) == str(2):
        print "Enter the brightness you want, select from [0, 50, 80, 100]"
        brightness = raw_input()
        led_brightness = brightness
        user_behavior = USER_PRESENCE
         
        light_control(float(brightness))
         
    update2thgspk(user_behavior, led_brightness)
         
def autoMode():
    global flag
    global absenceTime
    global user_behavior, led_brightness
     
    class state:
        def __init__(self, datatype, data):
            self.type = str(datatype)
            self.data = data
            self.time = datetime.datetime.now()
 
    user = state(datatype = "user", data = int(read_data("userlog.txt")))
    user_behavior = user.data
     
    if user.data == USER_ABSENCE:
        if flag == 0: #1st absence time
            flag = 1
            absenceTime = datetime.datetime.now()
        # turn off led when timeout reaches 15 minutes
        if ( datetime.datetime.now()-absenceTime ).total_seconds() < 900:
            time.sleep(1)
            pass
        elif ( datetime.datetime.now()-absenceTime ).total_seconds() > 900:
            light_control()
            led_brightness = 0
        else:
            print "Error in Sleep Mode"
            print (datetime.datetime.now()-absenceTime ).total_seconds()
     
    elif user.data == USER_PRESENCE: 
        flag = 0
        control = light_requirements()
        led_brightness = control
        light_control(control)
         
    update2thgspk(user_behavior, led_brightness)
