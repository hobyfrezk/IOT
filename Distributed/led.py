#reference: http://www.hivemq.com/blog/mqtt-client-library-paho-python

import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish
import datetime
import os

#IP = "169.254.205.192"
IP = "192.168.1.178"

# In each zone, we have 1 lightsensor, 1 PIR sensor, but we may have multiple control buttons.
DeviceID = "LED1"
ZoneID = "ZoneA"

Automode = 0
Manualmode = 1
UserPresence = 2
UserAbsence = 3

class led(object):

	def __init__(self, DeviceID = DeviceID, ZoneID = ZoneID, workingState = "0", AimIP = IP):
		self.DeviceID = DeviceID
		self.ZoneID = ZoneID
		self.workingMode = Automode
		self.workingState = workingState
		self.AimIP = AimIP
		self.client_id = "0000"+DeviceID

	#update brightness by working as a publisher, only sent once  for each brightness change, so set QoS = 2
	def updateBrightness(self)
		publish.single(topic = "/led/"+self.ZoneID+"/"+self.DeviceID, payload={ "DeviceID" = self.DeviceID, "workingState" = slef.workingState}, qos=2, hostname=IP,
           port=1883, client_id= self.client_id)


	#TBD change led brightness on raspberry Pi
	def setBrightness(self, brightness):
		self.workingState = brightness
		updateBrightness()



def on_connect(clientID, obj, flags, rc):
    print ("rc: " + str(rc))
    

# TBD, test clientID is of subscriber or puublisher
# the formate of msg is a dictionary	{"publisherID": number, "data": data}

def on_message_light(clientID, obj, msg):
	print str(msg.topic) + " " + str(msg.payload)

def on_message_button(clientID, obj, msg):
	print str(msg.topic) + " " + str(msg.payload)


def on_message_motion(clientID, obj, msg):
	print str(msg.topic) + " " + str(msg.payload)

def control():


subscriber = mqtt.Client(client_id = "0000"+DeviceID, clean_session=True)
subscriber.on_connect = on_connect
subscriber.message_callback_add("/sensor/light/"+ ZoneID, on_message_light)
subscriber.message_callback_add("/sensor/button/"+ ZoneID +"/#", on_message_button)
subscriber.message_callback_add("/sensor/motion/"+ ZoneID +"/#", on_message_motion)
subscriber.control = control

subscriber.connect(IP, 1883, 60)

#subscribe to light, button and PIR sensor
subscriber.subscribe([("/sensor/light/"+ZoneID+"/#", 0),("/sensor/button/"+ZoneID+"/#", 0),  ("/sensor/motion/"+ZoneID+"/#", 0)])
subscriber.loop_forever()


