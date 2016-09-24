import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import smbus
from smbus import SMBus
 
TIMESLEEP = 1
IP = "192.168.1.178"
 
TSL2561 = SMBus(1)
address = 0x39
control_on = 0x03
control_off = 0x00
 
def enable():
    TSL2561.write_byte(address, 0x80)
    TSL2561.write_byte(address, control_on)
 
def Light():    
    var = [5, 5, 5, 5]
    var = TSL2561.read_i2c_block_data(0x39, 0x8C)
    payloadlight = ((var[1]<<8) + var[0])
    publish.single("/light", payloadlight , qos=1, retain=True, hostname=IP)
     
def on_connect(mqttc, userdata, flags, rc):
        print("Connected with result code " +str(rc))
 
while True:
    enable()
    Light()
    time.sleep(TIMESLEEP)
