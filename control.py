import RPi.GPIO as GPIO
import time,datetime
import os


USER_PRESENCE = 1
USER_ABSENCE = 0
AUTOMODE = 2
INTERACTIVEMODE = 3

# used to read local data
def read_data (filename):
    os.chdir("/home/pi/IOT/temp")
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])

def writeLedlog(ledstate):
        os.chdir("/home/pi/IOT/temp")
        with open("ledlog.txt", "a") as f:
            f.write("\n"+ str(datetime.datetime.now())+ " " + str(ledstate))
    
# countrol led brightness, close led by default
def light_control(requirement = 0):

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    
    if requirement == 0:
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
        pass # all led have already been turned off at begining of this function
    
    if requirement == 1:
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
        
    if requirement == 2:
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
        
        
    if requirement == 3:
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(21,GPIO.LOW)
        
    if requirement ==4:
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(21,GPIO.HIGH)

    writeLedlog(requirement)



# the function set how light the led should be, darker outside, brighter led.
def light_requirements():
    light = read_data("lightlog.txt")
    if light  <100:
        return 4
    if light< 800:
        return 3
    if light  <1500:
        return 2
    if light  <3000:
        return 1
    else:
        return 0

def ControlMode():
    return read_data("modelog.txt")

    
def interactiveMode():
    print "===================================="
    print "Interactive mode:"
    print "1. go back to auto mode, push the button  then ENTER 1."
    print "2. Select brightness"
	
    command = str(raw_input())
    if command == "1":
        autoMode()
		
    elif command == "2":
        print "Enter the brightness you want, select from [1, 2, 3, 4] or 0 if you want to turn off all lights"
        brightness = raw_input()
        light_control(int(brightness))

    else:
        print "Wrong selection, please ENTER correct command. from [1, 2]"
		
def autoMode():
    global flag
    global absenceTime
    class state:
        def __init__(self, datatype, data):
            self.type = str(datatype)
            self.data = data
            self.time = datetime.datetime.now()

    user = state(datatype = "user", data = int(read_data("userlog.txt")))
    
    if user.data == USER_ABSENCE:
        if flag == 0: #1st absence time
            flag = 1
            absenceTime = datetime.datetime.now()
        # turn off led when timeout reaches 15 minutes
        if ( datetime.datetime.now()-absenceTime ).total_seconds() < 5:
            time.sleep(1)
            pass
        elif ( datetime.datetime.now()-absenceTime ).total_seconds() > 5:
            light_control()
        else:
            print "Error in Sleep Mode"
            print (datetime.datetime.now()-absenceTime ).total_seconds()
    
    elif user.data == USER_PRESENCE: 
        flag = 0
        control = light_requirements()
        light_control(control)

    time.sleep(0.5)
