import paho.mqtt.client as mqtt
import datetime
import os

#IP = "169.254.205.192"
IP = "192.168.1.178"

def on_connect(mqttc, obj, flags, rc):
    print ("rc: " + str(rc))
    
def on_message(mqttc, obj, msg):
    os.chdir("/home/pi/IOT/temp")
    print str(msg.topic) + " "+ str(msg.payload)
    if msg.topic[1:] == "user" or msg.topic[1:] == "mode" or msg.topic[1:] == "light": 
        with open(msg.topic[1:]+"log.txt", "a") as f:
            f.write("\n"+ str(datetime.datetime.now())+ " " + str(msg.payload))

subscriber = mqtt.Client(clean_session=True)
subscriber.on_connect = on_connect
subscriber.on_message = on_message

subscriber.connect(IP, 1883, 60)
subscriber.subscribe("#", 0)

subscriber.loop_forever()
