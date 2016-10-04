import httplib, urllib2
import os
import datetime
import json
import time

key = NXCLG7W3AQVRDBL1
ZoneID = "ZoneA"

class state(object):
	self.__NaturalLight = None
	self.__WorkingState = {"Led01":None , "Led02":None ,"Led03":None ,"Led04":None }

	# add new state to the end of channel, only set received ledID's state, others remain None
	def setState(self, "naturalLight" = None, "Led01" = None, "Led02" = None, "Led03" = None, "Led04"= None):
		if  data["naturalLight"] != None:
			self.__NaturalLight = data["naturalLight"]
			print "Natural light has been updated to %s" %self.__NaturalLight
			
		if  data["Led01"] != None:
			self.__WorkingState["Led01"] = data["Led01"]
			print "Led01 working state has been set to %s" %self.__WorkingState["Led01"]
			
		if  data["Led02"] != None:
			self.__WorkingState["Led02"] = data["Led02"]
			print "Led02 working state has been set to %s" %self.__WorkingState["Led02"]
			
		if  data["Led03"] != None:
			self.__WorkingState["Led03"] = data["Led03"]
			print "Led03 working state has been set to %s" %self.__WorkingState["Led03"]
			
		if  data["Led04"] != None:
			self.__WorkingState["Led04"] = data["Led04"]
			print "Led04 working state has been set to %s" %self.__WorkingState["Led04"]

	# update state to thingpeak
	def update(self):
		baseURL = 'https://api.thingspeak.com/update?api_key= %s' %key
		f = urllib2.urlopen(baseURL + "&field1=%s & field2=%s & field3=%s & field4=%s & field5=%s" %(self.__NaturalLight, 
				self.__WorkingState["Led01"], self.__WorkingState["Led02"], self.__WorkingState["Led03"], self.__WorkingState["Led04"]))
		print f.read()
		f.close()

def on_connect(client, obj, flags, rc):
	print ("client"+ client.data["ID"] + " is connected")
	# usbscriber all msg sent by light sensor and led., which light sensor gives us matural lightness and led
	subscriber.subscribe([("/sensor/light/" + ZoneID, 2)("/led/"+ZoneID+"/#", 2)])
#save comming message
def on_message_led(client, obj, msg):
	LedID = msg.topic[-5:]
	State = msg.payload
	client.data.setState(LedID = State)

def on_message_light(client, obj, msg):
	client.data.setState("naturalLight" = msg.payload)




def updateThread(client):
	client.data.update()
	time.sleep(15)
		

# Create a subscriber instance
subscriber = mqtt.Client(client_id = "thingspeakSubscriber", clean_session=True)
subscriber.on_connect = on_connect
subscriber.message_callback_add("/snesor/"+ZoneID+"/light/#", on_message_light)
subscriber.message_callback_add("/led/"+ZoneID+"/#", on_message_led)
subscriber.data = state()

s = Thread(target = updateThread())
s.start()
								
subscriber.loop_forever()
								
