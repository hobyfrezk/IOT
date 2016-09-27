from control import interactiveMode, autoMode, read_data, ControlMode
import RPi.GPIO as GPIO
import datetime


USER_ABSENCE = 0
USER_PRESENCE = 1
AUTOMODE = 2
INTERACTIVE = 3

if __name__ == "__main__":
    
    flag = 0 #used to flag absencetime in automode
    flag1 = 0 #used to flag automode text 
    try:
        while True:
            control = ControlMode()
            if control == AUTOMODE:
                if flag1 == 0:
                    flag1 = 1
                    print "You are woking in autoMode now"
                autoMode()
            else:
                flag1 = 0
                interactiveMode()
        

    except KeyboardInterrupt:
        GPIO.cleanup()
