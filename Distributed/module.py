# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime
import yaml
import numpy as np


LEDID = 1
ZoneID = 'zoneA'
timeoutTime = 900
Off = '0'
Automode = '1'
Manualmode = '2'

class Lamp(object):
    def __init__(self, ID = LEDID, ZoneID = ZoneID, workingState = Off, timeout = timeoutTime):
		self.__ID = LEDID
		self.__ZoneID = ZoneID
		self.__workingState = workingState
		self.__brightness = None
		self.__timeout = timeout
		self.__lastUserPresenceTime = None
		self.__naturalLight = None
		
    def getID(self):
        return self.__ID

    def getZoneID(self):
        return self.__ZoneID

    def getWorkingMode(self):
	return self.__workingMode

    def getWorkingState(self):
        return self.__workingState
    
    def getBrightness(self):
        return self.__brightness

    def getTimeOut(self):
        return self.__timeout

    def getUserPresenceTime(self):
        return self.__lastUserPresenceTime

    def getNaturalLight(self):
        return self.__naturalLight

    def setWorkingState(self, mode):
        if mode in (Off, Automode, Manualmode):
            self.__workingState = mode
            print "the working state has been set to %s correctly" %(mode)
            if mode == Off:
                self.setBrightness = 0
        else:
            print "Error in working state"
    
    def setBrightness(self, brightness):
        if brightness in range(0,100):
            self.__brightness = brightness
            print "the working brightness has been set to %s correctly" %(brightness)
        else:
            print "brightness out of range"    
            
    def renewPresenceTime(self):
	self.__lastUserPresenceTime = datetime.datetime.now()
 
    def setNaturalLight(self, state):
        self.__naturalLight = str(state)
        
        
        
# get actuators info from config file and return a matrix with all informations
def deviceMatrix():
    with open('config.json', 'r') as data_file:    
        config = yaml.safe_load(data_file)
        
    ActivatedZone = config['zone']['Activated']
    device = config['device'].keys()
    
    deviceMatrix = np.chararray(shape=(len(ActivatedZone)+1,len(device)+1), itemsize=100)
    deviceMatrix[:] = 0
    deviceMatrix[0,0] = 'ZoneID'
    i = 1
    for deviceType in device:
        deviceMatrix[0,i] = deviceType
        i = i+1
    
    i = 1
    for zone in ActivatedZone:
        deviceMatrix[i,0] = zone
        for j in range(1,len(device)+1):
            if zone in config['device'][deviceMatrix[0,j]].keys():
                deviceMatrix[i,j] = str(config['device'][deviceMatrix[0,j]][zone])
        i = i+1
    return deviceMatrix






