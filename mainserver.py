from Automode_light import automode 
from Interactive_mode import interactiveMode

#WIRING SETTING
LED = 4


USER_PRESENCE = 0
USER_ABSENCE = 1
AUTOMODE = 2
INTERACTIVE = 3

# used to read log file in local, we only care about neweast data, so read last number of file
def read_data(filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])

def ControlMode():
	return read_data(modelog.txt)

def main():
		try:
			control = ControlMode()
			if control == AUTOMODE:
				automode()
				
			elif control == INTERACTIVEMODE:
				interactivemode()

if __name__ == "main":
	main()

	
