# the lamp instance start with automode 
class Lamp(object):
	def __init__(self, ID = LEDID, ZoneID = ZoneID, workingMode = "Automode", workingState = "0", timeout = timeoutTime):
		self.__ID = ID
		self.__ZoneID = ZoneID
		self.__workingMode = workingMode
		self.__workingState = workingState
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

	def getTimeOut(self):
		return self.__timeout

	def getUserPresenceTime(self):
		return self.__lastUserPresenceTime

	def getNaturalLight(self):
		return self.__naturalLight
