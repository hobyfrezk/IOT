import httplib, urllib2
import os
import datetime
import json
import time

key = NXCLG7W3AQVRDBL1
ZoneID = "ZoneA"

class Node(object):
    def __init__(self, initdata):
        self.__data = initdata
        self.__next = None

    def getData(self):
        return self.__data

    def getNext(self):
        return self.__next

    def setData(self, newdata):
        self.__data = newdata

    def setNext(self, newnext):
        self.__next = newnext



class state(object):
	self.__NaturalLight = []
	self.__WorkingState = []

	# add new state to the end of channel
	def addnewState(self, data):
		self.__NaturalLight = data["naturalLight"]
		self.__WorkingState = data["workingState"]

	# update state to thingpeak
	def update(self):
		baseURL = 'https://api.thingspeak.com/update?api_key=%s' %key
		f = urllib2.urlopen(baseURL + "&field1=%s & field2=%s" %(self.__NaturalLight, self.__WorkingState))
		print f.read()
		f.close()


def on_message_led(client, obj, msg):
	deviceID = msg.topic[-5:]



def on_message_light(client, obj, msg):




def on_connect(client, obj, flags, rc):
    print ("client"+ client.data["ID"] + " is connected")
    # usbscriber all msg sent by light sensor and led., which light sensor gives us matural lightness and led
    subscriber.subscribe([("/sensor/"+ZoneID+"/light/#", 2)("/led/"+ZoneID+"/#", 2)])



# Create a subscriber instance
subscriber = mqtt.Client(client_id = "thingspeakSubscriber", clean_session=True)
subscriber.on_connect = on_connect
subscriber.message_callback_add(("/snesor/"+ZoneID+"/light/#", on_message_light)
subscriber.message_callback_add("/led/"+ZoneID+"/#", on_message_led)
subscriber.data