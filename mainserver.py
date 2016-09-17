# used to read log file in local, we only care about neweast data, so read last number of file
def read_data(filename):
    last_line = file(filename, "r").readlines()[-1]
    return int(last_line[27:])
    
# interactive mode
# ***sleep mode***
# ***adjustment brightness***
# ***go back to auto mode***
# ***turn off system***
def interactiveMode():

	
