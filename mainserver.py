AUTOMODE = 1
INTERACTIVE = 2


# used to read log file in local, we only care about neweast data, so read last number of file
def read_data(filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])

def ControlMode():
	return read_data(modelog.txt)



def



def

def main():
	while true:
		try:
			if controlMode == AUTOMODE:
				automode()
				
			elif controlMode == INTERACTIVEMODE:
				interactivemode()
				
	

	
