import paho.mqtt.client as mqtt
import threading
'''
used to monitor whole system
'''

# IP = "localhost"
#
#
# def on_connect(mqttc, obj, flags, rc):
#     print ("rc: " + str(rc))
#
#
# def on_message(mqttc, obj, msg):
#     print str(msg.topic) + " " + str(msg.payload)
#
#
# subscriber = mqtt.Client(clean_session=True)
# subscriber.on_connect = on_connect
# subscriber.on_message = on_message
# subscriber.data = None
#
# subscriber.connect(IP, 1883, 60)
# subscriber.subscribe("#", 0)
# while 1:
#     subscriber.loop_start()



IP = "localhost"


def on_connect(mqttc, obj, flags, rc):
    print ("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print str(msg.topic) + " " + str(msg.payload)


class client:
    def __init__(self):
        self.subscriber = mqtt.Client(clean_session=True)
        self.subscriber.on_connect = on_connect
        self.subscriber.on_message = on_message


def connect(subscriber):
    subscriber.subscriber.connect(IP, 1883, 60)
    subscriber.subscriber.subscribe("#", 0)
    while 1:
        subscriber.subscriber.loop_start()

a = client()
b = client()
c = client()

for lll in [a, b, c]:
    threading.Thread(target=connect, args=(lll,)).start()