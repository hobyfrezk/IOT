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
	def __init__(self, ID = DeviceID, ZoneID = ZoneID, workingMode = "OFF", workingState = "0", timeout = timeoutTime):
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


	def setWorkingMode(self, mode):
		if mode in ["Automode", "InteractiveMode", "OFF"]:
			self.__workingMode = mode

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
			light_control(state)
		else:
			print "Error in setting working state"


	def renewPresenceTime(self):
		self.__lastUserPresenceTime = datetime.datetime.now()

	def setNaturalLight(self, state):
		self.__naturalLight = str(state)


# callback for connect function and subscribe topic from device in same zone
def on_connect(client, obj, flags, rc):
    print ("client"+ client.data["ID"] + " is connected")
    subscriber.subscribe([("/sensor/light/%s/#" %(ZoneID), 2), ("/sensor/button/%s/#" %(ZoneID), 2), 
    	("/sensor/motion/%s/#" %(ZoneID), 2)])

def on_message_light(client, obj, msg):
	print "the natural brightness received is "+ str(msg.payload)
	client.setNaturalLight(msg.payload)
	client.control(client, "light", msg.payload)


def on_message_motion(client, obj, msg):
	print "motion detected"
	client.data.setUserPresence(datetime.datetime.now())
	client.control(client, "motion", msg.payload)


def on_message_button(client, obj, msg):
	client.control(client, "button", msg.payload)



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
		else:
			pass
			

	elif topic = "motion":
		if client.data.getWorkingMode = "Automode":
			client.data.control(topic = "light", payload = client.data.getNaturalLight)


	elif topic = "button":
		if payload == "autoMode":
			print "You are switching to autoMode"
			client.data.setWorkingMode("Automode")
			client.data.control(topic = "light", payload = client.data.getNaturalLight)
		elif payload in ["1", "2", "3", "4", "0"]:
			client.data.setWorkingMode("InteractiveMode")
			print "You are switching to interactiveMode, the working level is %s" %(payload)
			client.data.setWorkingState(int(payload))
		else:
			print "Wrong command"
	else:
		print "Wrong topic"
				


# used to trigger if user absence time beyond 15 minutes
def trigger():
	while True:
		if (datetime.datetime.now() - subscriber.data.getUserPresenceTime).totalseconds() < timeoutTime:
			subscriber.data.setWorkingState(0)

# used to publish working state to thingspeak so can be logged to internet
def updateWorkingState():
	while True:
		publish.single("/led/"+ZoneID+"/"+DeviceID+"/WorkState", client.data.getWorkingState, hostname=IP)
		time.sleep(20)


#control brightness by raspberry gpio port
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

	elif requirement == 1:
		GPIO.output(23,GPIO.HIGH)
		GPIO.output(12,GPIO.LOW)
		GPIO.output(16,GPIO.LOW)
		GPIO.output(21,GPIO.LOW)
        
	elif requirement == 2:
		GPIO.output(23,GPIO.HIGH)
		GPIO.output(12,GPIO.HIGH)
		GPIO.output(16,GPIO.LOW)
		GPIO.output(21,GPIO.LOW)
        
        
	elif requirement == 3:
		GPIO.output(23,GPIO.HIGH)
		GPIO.output(12,GPIO.HIGH)
		GPIO.output(16,GPIO.HIGH)
		GPIO.output(21,GPIO.LOW)
        
	elif requirement ==4:
		GPIO.output(23,GPIO.HIGH)
		GPIO.output(12,GPIO.HIGH)
		GPIO.output(16,GPIO.HIGH)
		GPIO.output(21,GPIO.HIGH)
	else:
    		print "WRONG COMMAND GIVEN"

# Create a subscriber instance
subscriber = mqtt.Client(client_id = "0000"+DeviceID, clean_session=True)
subscriber.on_connect = on_connect
client.on_subscribe = on_subscribe

subscriber.control = control

# set callback function for each topics that matters
subscriber.message_callback_add("/sensor/light/%s/#"+ %(ZoneID), on_message_light)
subscriber.message_callback_add("/sensor/button/%s/#" %(ZoneID), on_message_button)
subscriber.message_callback_add("/sensor/motion/%s/#" %(ZoneID), on_message_motion)

# create a property of a class Lamp to record data
Led1 = Lamp()
subscriber.data = Led1

# conntect to broker
subscriber.connect(IP, 1883, 60)

# create a thread to trigger user attendence and a publisher for sending working state
s = Thread(target = trigger, args = ())
s.start()
t = Thread(target = updateWorkingState, args = ())
t.start()

# start subscriber
subscriber.loop_forever()
