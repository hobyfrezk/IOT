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
		
		
