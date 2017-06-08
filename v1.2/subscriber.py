import paho.mqtt.client as mqtt
import threading
'''
used to monitor whole system
'''

IP = "localhost"


def on_connect(mqttc, obj, flags, rc):
    print ("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print str(msg.topic) + " " + str(msg.payload)


subscriber = mqtt.Client(clean_session=True)
subscriber.on_connect = on_connect
subscriber.on_message = on_message
subscriber.data = None

subscriber.connect(IP, 1883, 60)
subscriber.subscribe("#", 0)
while 1:
    subscriber.loop_start()