#reference: http://www.hivemq.com/blog/mqtt-client-library-paho-python

import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish
import datetime, time
import os
from threading import Thread
import json
from pprint import pprint
import RPi.GPIO as GPIO


with open('config.json') as data_file:    
	config = json.load(data_file)

IP = config["mqtt"]["ip_address"]
timeoutTime = config["sleep_timeout"] # 15 minutes

zoneID = config["zone"][1].key()[0]
DeviceID = config["device"]["LED"][zoneID][0]
PIRID = config["device"]["PIR"][zoneID][0]
buttonDeviceID = config["device"]["button"][zoneID][0]
LEDDeviceID = config["device"]["Lightsensor"][zoneID][0]

brightnessSetting = config['lamp_luminance']

class Lamp(object):
	def __init__(self, ID = DeviceID, ZoneID = ZoneID, workingMode = "Automode", workingState = "0", timeout = timeoutTime):
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
		if str(state) in ["0", "1", "2", "3", "4"]:
			self.__workingState = state

		if self.__workingState == state:
			print "the working state has been changed to %s correctly" %(state)
			light_control(int(state))
		else:
			print "Error in setting working state"

	def renewPresenceTime(self):
		self.__lastUserPresenceTime = datetime.datetime.now()

	def setNaturalLight(self, state):
		self.__naturalLight = str(state)


# callback for on_connect function and subscribe topic from devices in the same zone
def on_connect(client, obj, flags, rc):
	print ("client"+ str(client.data.getID())+ " is connected")
	subscriber.subscribe([("/sensor/"+zoneID+"light"+LEDDeviceID, 2), ("/sensor"+zoneID+"/button/"+buttonDeviceID, 2), ("/sensor/"+zoneID+"/motion"+motionDeviceID, 2)])

def on_message_light(client, obj, msg):
	message = json.loads(msg.payload)
	if msg.topic=="/sensor/"+zoneID+"light"+LEDDeviceID and message["DeviceID"] == LEDDeviceID:
		print "the natural brightness received is "+ message["data"]
		client.data.setNaturalLight(message["data"])
		client.control(client, topic = "light", payload = int(message["data"]))

def on_message_motion(client, obj, msg):
	message = json.loads(msg.payload)
	if msg.topic=="/sensor/"+zoneID+"/motion"+motionDeviceID and message["DeviceID"] == motionDeviceID:
		print "motion detected"
		client.data.renewPresenceTime()
		client.control(client, topic = "motion", payload = message)

def on_message_button(client, obj, msg):
	message = json.loads(msg.payload)
	if msg.topic=="/sensor"+zoneID+"/button/"+buttonDeviceID and message["DeviceID"] == buttonDeviceID:
		client.control(client, topic = "button", payload = message["data"])

def control(client, topic, payload):
	if topic == "light":
		if client.data.getWorkingMode() == "Automode":
			if int(payload) <lowNaturalBrightness:
				client.data.setWorkingState("4") 
			elif payload< MLowNaturalBrightness:
				client.data.setWorkingState("3") 
			elif payload  <MHighNaturalBrightness:
				client.data.setWorkingState("2") 
			elif payload  <HighNaturalBrightness:
				client.data.setWorkingState("1") 
			else:
				client.data.setWorkingState("0")
			

	elif topic == "motion":
		if client.data.getWorkingMode() == "Automode":
			client.control(client, topic = "light", payload = int(client.data.getNaturalLight()))


	elif topic == "button":
		if payload == "autoMode":
			print "You are switching to autoMode"
			client.data.setWorkingMode("Automode")
			client.control(client, topic = "light", payload = client.data.getNaturalLight())
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
		pass
		#if (datetime.datetime.now() - subscriber.data.getUserPresenceTime).totalseconds() < timeoutTime:
			#subscriber.data.setWorkingState(0)

# used to publish working state to thingspeak so can be logged to internet
def updateWorkingState():
	while True:
		messageMode = {"timestamp": time.asctime(), "DeviceID":deviceID, "data": subscriber.data.getWorkingMode()}
		messageState = {"timestamp": time.asctime(), "DeviceID":deviceID, "data": subscriber.data.getWorkingState()}
		publish.single("/led/"+ZoneID+"/"+DeviceID+"/Workmode", json.dumps(messageMode), hostname=IP)
		publish.single("/led/"+ZoneID+"/"+DeviceID+"/Workstate", json.dumps(messageState), hostname=IP)
		time.sleep(15)


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
subscriber = mqtt.Client(client_id = DeviceID, clean_session=False)
subscriber.on_connect = on_connect

subscriber.control = control

# set callback function for each topics that matters
subscriber.message_callback_add("/sensor/"+zoneID+"light"+LEDDeviceID, on_message_light)
subscriber.message_callback_add("/sensor"+zoneID+"/button/"+buttonDeviceID, on_message_button)
subscriber.message_callback_add("/sensor/"+zoneID+"/motion"+motionDeviceID, on_message_motion)

# create a property of a class Lamp to record data
subscriber.data = Lamp()

# conntect to broker
subscriber.connect(IP, 1883, 60)

# create a thread to trigger user attendence and a publisher for sending working state
#s = Thread(target = trigger, args = ())
#s.start()

t = Thread(target = updateWorkingState(), args = ())
t.start()

# start subscriber
subscriber.loop_forever()
