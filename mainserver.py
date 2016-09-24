from control import interactiveMode, autoMode
import RPi.GPIO as GPIO
 
 
USER_PRESENCE = 0
USER_ABSENCE = 1
AUTOMODE = 2
INTERACTIVE = 3
 
flag = 0
# used to read log file in local, we only care about neweast data, so read last number of file
def read_data(filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])
 
def ControlMode():
    return read_data("modelog.txt")
 
 
 
if __name__ == "__main__":
    flag = 0
    flag1 = 0
    try:
        while True:
            control = ControlMode()
            if control == AUTOMODE:
                if flag1 == 0:
                    flag1 = 1
                    print "You are woking in autoMode now"
                autoMode()    
            else:
                interactiveMode()
             
 
    except KeyboardInterrupt:
        GPIO.cleanup()
