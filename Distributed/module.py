# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime,yaml
import bidict
import numpy as np

import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish


def openconfig():
    with open('config.json', 'r') as data_file:    
        return yaml.safe_load(data_file)

# return device info as matrix form for each zone
def deviceMatrix(config):       
    ActivatedZone = config['zone']['Activated']
    device = config['device'].keys() 
    deviceMatrix = np.chararray(shape=(len(ActivatedZone)+1,len(device)+1), itemsize=100)
    deviceMatrix[:] = 0
    deviceMatrix[0,0] = 'ZoneID'
    i = 1
    for deviceType in device:
        deviceMatrix[0,i] = deviceType
        i = i+1    
    i = 1
    for zone in ActivatedZone:
        deviceMatrix[i,0] = zone
        for j in range(1,len(device)+1):
            if zone in config['device'][deviceMatrix[0,j]].keys():
                deviceMatrix[i,j] = str(config['device'][deviceMatrix[0,j]][zone])
        i = i+1

    return deviceMatrix      
        

def findindex(matrix, target):
    i,j=0,0
    for a in matrix:
        for b in a:
            if b == target:
                return [i,j]
            else:
                j = j+1
        j=0
        i=i+1    
    
        
class parameter():
    config = openconfig()
    
    device = deviceMatrix(config)
    mqttIP = config['mqtt']['ip_address']
    thingspeakKey = config['thingspeak']['thingspeak_key']
    sleepTimeout = config['sleep_timeout']
    Automode = config['state_index']['Automode']
    Manualmode = config['state_index']['Manualmode']
    Off = config['state_index']['Off']
    lightsensorAddress = config['lightsensor']['address']
    lightsensorControloff = config['lightsensor']['control_off']
    lightsensorControlon = config['lightsensor']['control_on']
    # define a bidirectional dictionary for luminance and working state
    entities = bidict.namedbidict('workingstate','luminance','state')
    workingstate = entities(config['lamp_luminance']) 
    
    
    
para = parameter()

ID = 'LED01'

class lamp(object):
    def __init__(self, ID = ID, config = para):
        self.config = config
        # get all relavent devices ID from config file
        row = findindex(config.device, ID)
        self.ID = ID
        self.ZoneID = config.device[row[0]]
        self.relaventDevice = config.device[row[0]]
        self.workMode = config.Off
        self.workState = config.workingstate.luminance_for['state0']
        self.timeout = config.sleepTimeout
        self.lastUserPresenceTime = None
        self.naturalLight = None
        
    subscriber = mqtt.Client(client_id = self.ID, clean_session=False)
        
# callback for on_connect function and subscribe topic from devices in the same zone
    def on_connect(client, obj, flags, rc):
	print ("client"+ str(client.data.getID())+ " is connected")
	subscriber.subscribe([("/sensor/"+zoneID+"light"+LEDDeviceID, 2), ("/sensor"+zoneID+"/button/"+buttonDeviceID, 2), ("/sensor/"+zoneID+"/motion"+motionDeviceID, 2)])
    
    def on_message(client, obj, msg):
        message = json.loads(msg.payload)
        if msg.topic 
        
        
    def on_message_light(client, obj, msg):
        message = json.loads(msg.payload)
        if msg.topic=="/sensor/"+zoneID+"light"+LEDDeviceID and message["DeviceID"] == LEDDeviceID:
            print "the natural brightness received is "+ message["data"]
            client.data.setNaturalLight(message["data"])
            client.control(client, topic = "light", payload = int(message["data"]))

    def on_message_motion(client, obj, msg):
	message = json.loads(msg.payload)
	if msg.topic=="/sensor/"+zoneID+"/motion"+motionDeviceID and message["DeviceID"] == motionDeviceID:
            print "motion detected"
            client.data.renewPresenceTime()
            client.control(client, topic = "motion", payload = message)

    def on_message_button(client, obj, msg):
        message = json.loads(msg.payload)
        if msg.topic=="/sensor"+zoneID+"/button/"+buttonDeviceID and message["DeviceID"] == buttonDeviceID:
            client.control(client, topic = "button", payload = message["data"])


# divice class is used for luminance sensor, PIR, and button
class device(object):
    def __init__(self, ID = ID, config = para):
        self.config = config
        # get all relavent devices ID from config file
        row = findindex(config.device, ID)
        self.ID = ID
        self.ZoneID = config.device[row[0]]
        self.relaventDevice = config.device[row[0]]
    
    def publish():
    
        
        
    def subscribe():
        
        








#==============================================================================
#     def setWorkingState(self, mode):
#         if mode in (self.config.Off, self.config.Automode, self.config.Manualmode):
#             self.workingState = mode
#             print "the working state has been set to %s correctly" %(mode)
#             if mode == self.config.Off:
#                 self.setBrightness(0)
#         else:
#             print "Error in working state"
#      
#     def setBrightness(self, brightness):
#         if brightness in self.config.workingstate.state_for.keys():
#             self.__brightness = brightness
#             print "the working brightness has been set to %s correctly" %(brightness)
#         else:
#             print "brightness out of range"    
#     
#     def renewPresenceTime(self):
#         self.__lastUserPresenceTime = datetime.datetime.now()
#      
#     def setNaturalLight(self, state):
#         self.__naturalLight = str(state)
#==============================================================================


