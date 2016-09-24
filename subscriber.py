import paho.mqtt.client as mqtt
import datetime
 
IP = "192.168.1.178"
 
def on_connect(mqttc, obj, flags, rc):
    print ("rc: " + str(rc))
def on_message(mqttc, obj, msg):
    print str(msg.topic) + " "+ str(msg.payload)
    f = open(msg.topic[1:]+"log.txt", "a")
    f.write("\n"+ str(datetime.datetime.now())+ " " + str(msg.payload))
    f.close
 
subscriber = mqtt.Client(clean_session=True)
subscriber.on_connect = on_connect
subscriber.on_message = on_message
 
subscriber.connect(IP, 1883, 60)
subscriber.subscribe("#", 0)
 
subscriber.loop_forever()
