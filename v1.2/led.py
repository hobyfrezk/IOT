import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from control import *
import threading


class Lamp(object):
    # power = {"ON", "OFF"}
    # workingMode = {"AUTO", "MANUAL"}
    # workingState = {"0", "1", "2", "3", "4"}
    def __init__(self, zone, ID):
        self.zone = zone
        self.ID = ID
        self.power = 'OFF'
        self.mode = 'AUTO'
        self.state = '0'
        self.pir_time = time.time()
        self.surrounding_light = '0'

    @property
    def device_ID(self):
        return self.zone + self.ID

    def set_power(self, power):
        self.power = power
        print "led (%s) has been turned %s." % (self.device_ID, self.power)

    def set_mode(self, value):
        self.mode = value
        print "led (%s) working mode has been set to (%s)." % (self.device_ID, self.mode)

    def set_state(self, state):
        self.state = state
        print "led (%s), mode: (%s), state: (%s)" % (self.device_ID, self.mode, self.state)
        # set led brightness on raspberry
        # light_control(int(state))

    def set_pir_time(self, time):
        self.pir_time = time
        print "led (%s) pir time updated." % self.device_ID

    def set_surrounding_light(self, value):
        self.surrounding_light = value
        print "led (%s) surrounding light value updated: (%s)." % (self.device_ID, value)


class led_client(Lamp):
    def __init__(self, zone, ID):
        super(led_client, self).__init__(zone, ID)
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

    def __repr__(self):
        return 'led client: zone(%s), id(%s).' % (self.zone, self.ID)

    def on_connect(self, mqttc, obj, flags, rc):
        print 'led ' + self.device_ID + ' is running... '

    def on_message(self, mqttc, obj, msg):
        topic, data = [msg.topic, json.loads(msg.payload)]
        if 'led' in topic:
            pass
        else:
            # double check if the message is sent correctly
            if data['device_ID'] == self.device_ID:
                control(self, topic, data)
                self.publish()

    @property
    def gen_payload(self):
        return {"timestamp": time.time(), "mode": self.mode, "state": self.state, "device_ID": self.device_ID}

    def publish(self):
        publish.single("/led/" + self.zone + '/' + self.ID, json.dumps(self.gen_payload), hostname='localhost')


def thread_job(led):
    led.mqttc.connect('localhost', 1883, 60)
    led.mqttc.subscribe("#", 0)
    led.mqttc.loop_forever()


def main():
    with open('config.json') as data_file:
        config = json.load(data_file)

    devices = config['DeviceID']
    device_list = []

    for zone in devices.keys():
        for node in devices[zone]:
            device_list.append([zone, node])

    lights = [led_client(zone, node) for [zone, node] in device_list]

    for light in lights:
        threading.Thread(target=thread_job, args=(light,)).start()

if __name__ == '__main__':
    main()
