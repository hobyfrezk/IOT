import paho.mqtt.client as mqtt
import datetime
import os

#IP = "169.254.205.192"
IP = "192.168.1.178"

DeviceID = 1
DeviceZone = "ZoneA"

def on_connect(mqttc, obj, flags, rc):
    print ("rc: " + str(rc))
    
def on_message(mqttc, obj, msg):
