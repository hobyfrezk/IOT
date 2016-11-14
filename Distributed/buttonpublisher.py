'''
Created on Mar 12, 2016

@author: toor
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from threading import Thread
import time



with open('config.json') as data_file:    
        data = json.load(data_file)


zoneID = data["DeviceID"].key()[0]
DeviceID = data["DeviceID"][zoneID]["Button"][0]
ledID = data["DeviceID"][zoneID]["led"][0]
IP = data["Parameters"]["IP"]

def on_connect(mqttc, userdata, flags, rc):
        print("Connected with result code " +str(rc))

def on_message(mqttc, obj, msg):
        # double check topic and payload if the received msg is from the led that button is working for
        message = json.loads(msg.payload)
        if msg.topic=="/led/"+zoneID+"/"+ledID+"/Workmode" and message["DeviceID"] == ledID:
                mqttc.data = message["data"]



button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN)

def trigger():
        while True:
                input_value = GPIO.input(button_pin)
                # button pressed
                if input_value==False:
                        if mqttc.data == "Automode":
                                print "Switching to interactive mode .."
                                print "Choose a brightness level [0, 1, 2, 3, 4]: "
                                command = raw_input()
                                message = {"timestamp"time.asctime():, "data": command, "deviceID": DeviceID}
                                publish.single("/sensor/"+zoneID+"button/"+DeviceID, json.dumps(message), hostname =IP)

                        elif mqttc.data == "InteractiveMode":
                                command = "autoMode"
                                message = {"timestamp"time.asctime():, "data": command, "deviceID": DeviceID,}
                                publish.single("/sensor"+zoneID+"/button/"+DeviceID, json.dumps(message), hostname = IP)   
                        else:
                                pass
                else:
                        pass
                time.sleep(1)

mqttc = mqtt.Client(client_id="button", clean_session=False)
mqttc.connect(IP, 1883, 60)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.subscribe("/led/"+zoneID+"/"+ledID+"/Workmode",2)
mqttc.data = None

s = Thread(target = trigger)
s.start()
mqttc.loop_forever()

  
