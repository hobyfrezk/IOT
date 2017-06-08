import time, json
import paho.mqtt.publish as publish
import threading
import paho.mqtt.client as mqtt
from control import *

message = {"timestamp": time.time(), "switch": 5, "device_ID": "zone3node1"}
publish.single("/switch/zone3/node1", json.dumps(message), hostname='localhost')


