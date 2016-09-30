#reference: http://www.hivemq.com/blog/mqtt-client-library-paho-python

import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish
import datetime
import os
from threading import Thread


#IP = "169.254.205.192"
IP = "192.168.1.178"

# In each zone, we have 1 lightsensor, 1 PIR sensor, but we may have multiple control buttons.
DeviceID = "LED1"
ZoneID = "ZoneA"
timeoutTime = 900 # 15 minutes

Automode = 0
Manualmode = 1
UserPresence = 2
UserAbsence = 3

class Lamp(object):
	# workingMode = {"Automode", "InteractiveMode", "OFF" }
	# workingState = {"0", "1", "2", "3", "4"}
	def __init__(self, "ID" = DeviceID, "ZoneID" = ZoneID, "workingMode" = "OFF", "workingState" = "0", "timeout" = timeoutTime):
		self.__ID = DeviceID
		self.__ZoneID = ZoneID
		self.__workingMode = "OFF"
		self.__workingState = "0"
		self.__timeout = timeoutTime
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


	def setWorkingMode(self, mode):
		if mode in ["Automode", "InteractiveMode", "OFF"]:
			self.__workingMode = mode
			func(CHANGE OUTPUT IN RASPBERRYPI)

		if self.__workingMode == mode:
			print "the working mode has been set to %s correctly" %(mode)
		else:
			print "Error in setting working mode"
		if self.__workingMode == "OFF":
			self.setWorkingState("0")



	def setWorkingState(self, state):
		if state in ["0", "1", "2", "3", "4"]:
			self.__workingState = state

		if self.__workingState == state:
			print "the working state has been changed to %s correctly" %(state)
			func(CHANGE OUTPUT IN RASPBERRYPI)
		else:
			print "Error in setting working state"


	def setUserPresence(self):
		self.__lastUserPresenceTime = datetime.datetime.now()

	def setNaturalLight(self, state):
		self.__naturalLight = str(state)



def on_connect(client, obj, flags, rc):
    print ("client"+ client.data["ID"] + "connected")
    subscriber.subscribe([("/sensor/light/%s/#" %(ZoneID),, 2), ("/sensor/button/%s/#" %(ZoneID), 2), 
    	("/sensor/motion/%s/#" %(ZoneID), 2)])

# the structure of msg is a dictionary	
# for light sensor {"brightness": data}
# for motion sensor {"detected time": time()}
# for button {"mode": mode, "data": brightness/empty}

def on_message_light(client, obj, msg):
	print str(msg.topic) + " " + str(msg.payload)
	client.control(client, "light", msg.payload)

def on_message_button(client, obj, msg):
	print str(msg.topic) + " " + str(msg.payload)
	client.control(client, "button", msg.payload)


def on_message_motion(client, obj, msg):
	print str(msg.topic) + " " + str(msg.payload)
	client.control(client, "motion", msg.payload)

def control(client, topic, payload):
	if topic = "light":
		if client.data.getWorkingMode = "Automode":
			if payload  <100:
	        	client.data.setWorkingState(4) 
		    elif payload< 800:
		        client.data.setWorkingState(3) 
		    elif payload  <1500:
		        client.data.setWorkingState(2) 
		    elif payload  <3000:
		        client.data.setWorkingState(1) 
		    else:
		        client.data.setWorkingState(0) 
			

	elif topic = "motion":
		client.data.setUserPresence(datetime.datetime.now())
		if client.data.getWorkingMode = "Automode":
			client.data.control(topic = "light", payload = client.data.getNaturalLight)

	elif topic = "button":
		if payload["mode"] == Automode:
			client.data.setWorkingMode = "Automode"
			client.data.control(topic = "light", payload = client.data.getNaturalLight)
		elif  payload["mode"] == InteractiveMode:
			client.data.setWorkingState = payload["data"]
		else:
			print "Wrong command"
	else:
		print "Wrong topic"
				



def trigger():
	if (datetime.datetime.now() - subscriber.data.getUserPresenceTime).totalseconds() < timeoutTime :
		subscriber.data.setWorkingMode(OFF)




subscriber = mqtt.Client(client_id = "0000"+DeviceID, clean_session=True)
subscriber.on_connect = on_connect
client.on_subscribe = on_subscribe

subscriber.control = control

# set callback function for each topics
subscriber.message_callback_add("/sensor/light/%s/#"+ %(ZoneID), on_message_light)
subscriber.message_callback_add("/sensor/button/%s/#" %(ZoneID), on_message_button)
subscriber.message_callback_add("/sensor/motion/%s/#" %(ZoneID), on_message_motion)

# create a instance for data
Led1 = Lamp
subscriber.data = Led1

subscriber.connect(IP, 1883, 60)
subscriber.loop_forever()


# create a thread to trigger user attendence
s = Thread(target=trigger, args=())
s.start()

