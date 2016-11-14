'''
Created on Feb 11, 2016

@author: toor
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time, json, random


with open('config.json') as data_file:    
	data = json.load(data_file)

zoneID = data["DeviceID"].key()[0]
IP = data["Parameters"]["IP"]
deviceID = data["DeviceID"][zoneID]["PIR"][0]
 

def on_connect(mqttc, userdata, flags, rc):
        print("Connected with result code " +str(rc))
         
mqttc = mqtt.Client(client_id="motionpublisher", clean_session=False)
mqttc.connect_async(IP, 1883, 60)
mqttc.on_connect = on_connect

def message():
	global x
	x = random.randint(3, 5)
	return {"timestamp": time.asctime(), "DeviceID":deviceID, "msg": "This is a motion detected alert"}

while True:
    publish.single("/sensor/"+zoneID+"/motion"+deviceID, json.dumps(message()), hostname=IP)
    time.sleep(x)
