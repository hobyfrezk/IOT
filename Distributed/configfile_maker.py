# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:45:33 2016

@author: Wang
"""

import json

configuration = {'mqtt': {'ip_address': '192.168.1.178'}, 
	  'thingspeak': {'thingspeak_key': 'NXCLG7W3AQVRDBL1'},
	  'state_index': {'Off':'0', 'Automode': '1', 'Manualmode': '2'},
	  'sleep_timeout': '900' ,
	  'zone': {'Activated': ['ZoneA', 'ZoneB'], 'Disactivated': []},
	  'device': {'LED': {'ZoneA': 'LED01', 'ZoneB': 'LED02'},
		     'PIR': {'ZoneA': 'PIR01'},
		     'LSensor': {'ZoneA': 'LSensor01'},
		     'button': {'ZoneA': 'button01'}},			 
	  'lamp_luminance': {'1000':'state1', '600': 'state2', '400':'state3', '100': 'state4', '0': 'state0'},
	  'lightsensor': {'address': '0x39','control_on': '0x03','control_off': '0x00'}
	 }

with open('config.json', 'w') as f:
    json.dump(configuration, f)
