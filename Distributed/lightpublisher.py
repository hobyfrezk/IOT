'''
Created on Mar 7, 2016

@author: toor
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import smbus
from smbus import SMBus


with open('config.json') as data_file:    
    data = json.load(data_file)

zoneID = data["DeviceID"].key()[0]
IP = data["Parameters"]["IP"]
DeviceID = data["DeviceID"][zoneID]["Lightsensor"][0]

TSL2561 = SMBus(1)
address = data["LightSensor"]["address"]
control_on = data["LightSensor"]["control_on"]
control_off = data["LightSensor"]["control_off"]

def enable():
    TSL2561.write_byte(address, 0x80)
    TSL2561.write_byte(address, control_on)

def Light():    
    var = [5, 5, 5, 5]
    var = TSL2561.read_i2c_block_data(0x39, 0x8C)
    payloadlight = ((var[1]<<8) + var[0])
    return payloadlight
    
def on_connect(mqttc, userdata, flags, rc):
        print("Connected with result code " +str(rc))

mqttc = mqtt.Client(client_id=DeviceID, clean_session=False)
mqttc.connect_async(IP, 1883, 60)
mqttc.on_connect = on_connect
mqttc.loop_start()

while True:
    enable()
    message = {"timestamp"time.asctime():, "data": Light(), "DeviceID": DeviceID}
    publish.single("/sensor/"+zoneID+"light"+DeviceID, json.dumps(message), retain=True, hostname=IP)
    time.sleep(2)
