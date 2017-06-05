import json
from datetime import datetime
import paho.mqtt.client as mqtt


class Lamp(object):
    # power = {"ON", "OFF"}
    # workingMode = {"AUTO", "MANUAL"}
    # workingState = {"0", "1", "2", "3", "4"}
    def __init__(self, device_id):
        self.ID = device_id
        self.power = 'OFF'
        self.mode = 'AUTO'
        self.state = '0'
        self.pir_time = datetime.now()
        self.natural_light = None

    def set_power(self, power):
        self.power = power
        print "led (%s) has been turned (%s)" % (self.ID, self.power)

    def set_mode(self, mode):
        self.mode = mode
        print "led (%s) working mode has been set to (%s)" % (self.ID, self.mode)

    def set_state(self, state):
        self.state = state
        print "led (%s) working state has been changed to %s correctly" % (self.ID, self.state)
        # set led brightness on raspberry
        # light_control(int(state))

    def set_pir_time(self):
        self.pir_time = datetime.now()
        print "led (%s) pir time has been updated" % self.ID

    def set_natural_light(self, value):
        self.natural_light = value
        print "led (%s) natural light value has been updated" % self.ID


def auto_mode(natural_light, pir_time):
    # to be removed into config file
    # [
    #   ...
    #   state, (low_bound, up_bound)
    #   ...
    # ]
    control_table = [
        ('0', (0, 100)),
        ('1', (101, 800)),
        ('2', (801, 1500)),
        ('3', (1501, 3000)),
        ('4', (3001, 99999)),
    ]
    # check if user presence:
    time_difference = datetime.now() - pir_time
    if time_difference.seconds < 900:
        presence = 1
    else:
        presence = 0

    if presence:
        for state, (low_bound, up_bound) in control_table:
            if low_bound <= natural_light <= up_bound:
                return state
    else:
        return str(0)


def manual_mode(value):
    return value


class Control(Lamp):
    def __init__(self, led_id):
        super(Control, self).__init__(device_id=led_id)

    def control(self, msg):
        message = json.loads(msg.payload)
        if 'light' in msg.topic:
            self.natural_light = message['data']
            if self.mode == 'AUTO':
                self.set_state(auto_mode(self.natural_light, self.pir_time))

        elif 'switch' in msg.topic:
            self.mode = message['data']

            if self.mode == 'AUTO':
                self.set_state(auto_mode(message['data'], self.pir_time))
            elif self.mode == 'MANUAL':
                manual_mode(message['state'])

        elif 'pir' in msg.topic:
            self.pir_time = datetime.now()


class led_client(Control):
    def __init__(self, client_id):
        super(led_client, self).__init__(led_id=client_id)
        self._mqttc = mqtt.Client(self.ID)
        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect

    # callback for on_connect function and subscribe topic from devices in the same zone
    def on_connect(self, client, obj, flags, rc):
        print "led (%s) is now connected to broker." % self.ID

        # to be complete with topic info.
        # self._mqttc.subscribe([("/sensor/" + zoneID + "/light/" + LEDDeviceID, 2), ("/sensor" + zoneID + "/button/" +
        # buttonDeviceID, 2), ("/sensor/" + zoneID + "/motion" + motionDeviceID, 2)]))

    def on_message(self, client, obj, msg):
        message = json.loads(msg.payload)
        Control.control(message)

    def thingspeak(self):
        pass


